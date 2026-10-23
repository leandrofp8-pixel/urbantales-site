# Smart download link

Public URL after deployment: https://urbantales.net/download/

TikTok paid campaign:
https://urbantales.net/download/?utm_source=tiktok&utm_medium=paid_social&utm_campaign=tiktok-launch

Routes iPhone/iPod/iPad (including desktop-mode iPadOS) to Apple's listing, Android to Google Play, and leaves other devices on a two-store chooser. Store buttons remain available when automatic navigation is blocked or JavaScript is disabled. No third-party scripts or network requests before navigation. Use the trailing slash to avoid a hosting redirect.

Attribution: Apple uses the existing provider token and `utm_campaign` as its campaign token (40-character maximum). Play receives URL-encoded UTM source, medium, campaign, optional content and term as its install referrer. `src` is supported as a source alias. These tags do not constitute TikTok conversion tracking or deferred deep linking. Arbitrary query parameters (including click IDs) are not forwarded. Store reporting is subject to each store's thresholds and attribution rules.

Validate with `node tests/download-redirect.cjs`. Before spending on the ad, test the deployed URL inside TikTok on real iOS and Android devices; automated user-agent tests cannot guarantee app switching inside TikTok. If the ad setup requires a direct store URL, use its OS-specific store destination instead.
