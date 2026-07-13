# tracking-pixel-finder

Install the required libraries 
```bash
pip3 install -r requirements.txt
```

```bash
sudo apt-get update && sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libnss3 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2t64 libatspi2.0-0 libxshmfence1 libx11-xcb1 libxcb-dri3-0 libgtk-3-0
```


# setup playwrite
```bash
playwright install --with-depts
```
# (optional) Replace the list items in "domains_to_check[]" with your own list to see if they contain tracking pixels. 

# run script
```badh
python3 tracking_pixel_finder.py
```