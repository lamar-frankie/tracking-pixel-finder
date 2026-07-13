# tracking-pixel-finder

This script scans a list of domains and reports likely tracking pixels and analytics requests.

## Prerequisites

Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

Install the browser dependencies required by Playwright on Linux:
```bash
sudo apt-get update && sudo apt-get install -y \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libnss3 \
  libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libxkbcommon0 \
  libpango-1.0-0 libcairo2 libasound2t64 libatspi2.0-0 libxshmfence1 \
  libx11-xcb1 libxcb-dri3-0 libgtk-3-0
```

Install the Playwright browser runtime:
```bash
playwright install --with-deps
```

## Run locally

From the project directory, run:
```bash
python3 tracking_pixel_finder.py
```

## Customize the scan

Optional: replace the items in the `domains_to_check` list inside `tracking_pixel_finder.py` with your own domains to scan.
