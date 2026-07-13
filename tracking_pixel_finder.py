import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse


class PlaywrightLaunchError(RuntimeError):
    """Raised when Chromium cannot be launched for scanning."""

# A basic blocklist of known tracking networks (you can expand this with EasyPrivacy lists)
KNOWN_TRACKERS = [
    "facebook.com/tr",         # Meta/Facebook Pixel
    "connect.facebook.net", 
    "google-analytics.com",    # Google Analytics
    "doubleclick.net",         # Google Ads
    "googletagmanager.com", 
    "bat.bing.com",            # Microsoft Ads
    "pixel.wp.com",            # WordPress Pixel
    "criteo.com",              # Criteo Retargeting
    "ads.linkedin.com"         # LinkedIn Insight Tag
]

async def check_domain_for_pixels(domain):
    async with async_playwright() as p:
        url = f"https://{domain}"
        print(f"\nScanning: {url}")

        try:
            # Launch a headless Chromium browser
            browser = await p.chromium.launch(headless=True)
        except Exception:
            print(
                "  [!] Playwright could not launch Chromium. Install the missing system "
                "libraries and browser dependencies, then run: playwright install --with-deps"
            )
            return None

        try:
            context = await browser.new_context()
            page = await context.new_page()

            found_trackers = []

            # Intercept and analyze every network request before it is sent
            page.on("request", lambda request: analyze_request(request, domain, found_trackers))

            try:
                # wait_until="networkidle" ensures we wait for delayed tracking scripts to fire
                await page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception as e:
                print(f"  [!] Failed to fully load or timed out: {e}")

            await browser.close()

            # Output the results
            unique_trackers = sorted(set(found_trackers))
            if unique_trackers:
                print(f"  [!] Found {len(unique_trackers)} trackers/pixels:")
                for tracker in unique_trackers:
                    print(f"      - {tracker}")
            else:
                print("  [*] No known tracking pixels detected.")

            return {
                "url": url,
                "trackers": unique_trackers,
            }
        finally:
            try:
                await browser.close()
            except Exception:
                pass

def analyze_request(request, main_domain, found_trackers):
    req_url = request.url
    parsed_url = urlparse(req_url)
    req_domain = parsed_url.netloc
    
    # 1. Check if the request URL contains known tracking domains
    for tracker in KNOWN_TRACKERS:
        if tracker in req_url:
            found_trackers.append(f"Known Tracker: {tracker}")
            return

    # 2. Heuristic Check: Look for suspicious 3rd-party image requests
    # Trackers often use 1x1 images with long query strings containing user IDs
    if req_domain and main_domain not in req_domain:
        if request.resource_type == "image":
            suspicious_params = ["uid=", "id=", "trk=", "session=", "pixel"]
            if "?" in req_url and any(param in req_url.lower() for param in suspicious_params):
                # Truncate the URL for cleaner console output
                truncated_url = (req_url[:80] + '...') if len(req_url) > 80 else req_url
                found_trackers.append(f"Suspicious 3rd-Party Pixel: {truncated_url}")

async def main():
    domains_to_check = [
        # "academy.takeflightinteractive.com",
        # "flitesim.com",
        # "flightsim.to",
        # "flightsimbuilder.com",
        # "forums.flightsimulator.com",
        # "forums.x-plane.org",
        # "navigraph.com",
        # "ruckerworks.com",
        # "virtualtours.senecapolytechnic.ca",
        # "x-plane.to",
        # "autonomous.ai",
        # "belkin.com",
        # "bhphotovideo.com",
        # "chairpartsonline.com",
        # "corsair.com",
        # "elgato.com",
        # "legacy.coolermaster.com",
        # "linustechtips.com",
        # "makerworld.com",
        # "marketplace.elgato.com",
        # "mtsim.com",
        # "nextlevelracing.com",
        # "shop.busyboxsign.com",
        # "smallrig.com",
        "subinsider.com",
        "tesmart.com",
        "us.govee.com",
        "us.switch-bot.com",
        "1800contacts.com",
        "amazon.com",
        "carsandstays.delta.com",
        "delta.com",
        "hotwire.com",
        "ups.com",
        "walmart.com",
        "511tactical.com",
        "ballisticdefence.com",
        "lapolicegear.com",
        "palmettostatearmory.com",
        "propper.com",
        "safariland.com",
        "claude.ai",
        "github.com",
        "google.com"
    ]
    
    for domain in domains_to_check:
        await check_domain_for_pixels(domain)

if __name__ == "__main__":
    asyncio.run(main())