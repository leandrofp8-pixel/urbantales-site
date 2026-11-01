"""
Publishes a rendered carousel batch to Instagram via the Graph API.

Usage:
    IG_USER_ID=... IG_ACCESS_TOKEN=... python3 ig_publish.py path/to/batch.json

Slides must already be pushed to main so GitHub Pages serves them at
https://urbantales.net/carousel/drafts/<city>/ (Instagram fetches each image by URL).
For a batch with "lang": "es" it posts the slide-*.es.png set. Caption comes from the batch.

Instagram's API can't attach music: add it in the app after publishing.
"""
import sys, os, json, time, urllib.request, urllib.parse, urllib.error

# Tokens from "Instagram API with Instagram Login" use graph.instagram.com; Facebook-Page tokens use graph.facebook.com.
GRAPH = os.environ.get("IG_GRAPH", "https://graph.instagram.com/v21.0")
BASE = "https://urbantales.net/carousel/drafts"
SLIDES = ["1-cover"] + [f"{i+1}-fact{i}" for i in range(1, 8)] + ["9-cta"]

def call(method, path, tries=3, **params):
    """Graph API call. Instagram fetches each slide image while answering, so a slow answer is common:
    2026-10-18/24/31 a single 60 s read timeout cancelled the whole carousel. Retries cover timeouts and
    dropped connections; a fresh container is harmless (only media_publish posts anything)."""
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{GRAPH}/{path}"
    for attempt in range(1, tries + 1):
        if method == "GET":
            req = urllib.request.Request(f"{url}?{data.decode()}")
        else:
            req = urllib.request.Request(url, data=data, method="POST")
        try:
            return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            sys.exit(f"{method} {path} failed: {e.read().decode()}")
        except (TimeoutError, OSError) as e:  # socket.timeout, connection reset, URLError
            if attempt == tries:
                raise
            print(f"{method} {path}: {e!r}, retrying ({attempt}/{tries - 1})", flush=True)
            time.sleep(10 * attempt)

def wait_ready(container_id):
    for _ in range(30):
        status = call("GET", container_id, fields="status_code")["status_code"]
        if status == "FINISHED":
            return
        if status == "ERROR":
            sys.exit(f"container {container_id} failed processing")
        time.sleep(2)
    sys.exit(f"container {container_id} not ready after 60s")

def main():
    batch_path = sys.argv[1]
    spec = json.load(open(batch_path))
    slug = os.path.basename(os.path.dirname(os.path.abspath(batch_path)))
    lang = spec.get("lang", "en")
    sfx = "" if lang == "en" else f".{lang}"
    user = os.environ["IG_USER_ID"]

    children = []
    for s in SLIDES:
        url = f"{BASE}/{slug}/slide-{s}{sfx}.png"
        if urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30).status != 200:
            sys.exit(f"not live yet: {url}")
        cid = call("POST", f"{user}/media", image_url=url, is_carousel_item="true")["id"]
        children.append(cid)
        print(f"container slide-{s}{sfx}: {cid}")
    for cid in children:
        wait_ready(cid)

    carousel = call("POST", f"{user}/media", media_type="CAROUSEL",
                    children=",".join(children), caption=spec["caption"])["id"]
    wait_ready(carousel)
    # Never retry the publish call itself: it may have gone out without an answer (seen with a Reel
    # on 2026-10-20). Ask the container instead, so a lost answer is not reported as a failure.
    try:
        media_id = call("POST", f"{user}/media_publish", tries=1, creation_id=carousel)["id"]
    except (TimeoutError, OSError):
        for _ in range(12):
            time.sleep(10)
            try:
                if call("GET", carousel, fields="status_code").get("status_code") == "PUBLISHED":
                    link = call("GET", f"{user}/media", fields="permalink", limit=1)["data"][0]["permalink"]
                    print(f"published: {link} (publish call timed out, but the container is PUBLISHED)")
                    return
            except (TimeoutError, OSError):
                pass
        raise
    link = call("GET", media_id, fields="permalink")["permalink"]
    print(f"published: {link}")

if __name__ == "__main__":
    main()
