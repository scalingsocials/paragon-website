"""Download each image in images/manifest.txt, resize and save as compressed WebP."""
import io, sys, urllib.request
from PIL import Image

MAX = 1000      # longest side in px
QUALITY = 78
failed = []
for line in open("images/manifest.txt"):
    line = line.strip()
    if not line:
        continue
    name, url = line.split(" ", 1)
    src = url + ("&" if "?" in url else "?") + "width=1400"
    try:
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=60).read()
        im = Image.open(io.BytesIO(raw))
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        im.thumbnail((MAX, MAX), Image.LANCZOS)
        im.save(f"images/{name}", "WEBP", quality=QUALITY, method=6)
        print(f"{name}: {len(raw)//1024} KB -> {im.size}")
    except Exception as e:  # keep going, report at the end
        failed.append(f"{name} {url} {e}")
        print(f"FAILED {name}: {e}")
open("images/failed.txt", "w").write("\n".join(failed))
