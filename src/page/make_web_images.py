"""Make web-sized WebP copies of the Blender renders.  Run from project root: python3 src/page/make_web_images.py

The renders use a shadow catcher, so the floor is semi-transparent. Its alpha is faded to zero
towards the image edges so no rectangle shows on the page; fully opaque pixels (Dino) stay untouched."""
import os
from PIL import Image, ImageChops
SRC, DST = 'assets/renders', 'assets/web'
SIZES = {'dino_hero': 1100, 'dino_front_blank': 1100, 'dino_back': 800, 'dino_exploded': 1400}
os.makedirs(DST, exist_ok=True)

def edge_mask(W, H, n=200):
    m = Image.new('L', (n, n)); px = m.load()
    for y in range(n):
        for x in range(n):
            dx, dy = (x + .5) / n * 2 - 1, (y + .5) / n * 2 - 1
            d = (dx * dx + dy * dy) ** .5
            px[x, y] = int(255 * max(0., min(1., (0.92 - d) / 0.32)))
    return m.resize((W, H), Image.BILINEAR)

for name, w in SIZES.items():
    p = os.path.join(SRC, name + '.png')
    if not os.path.exists(p): print('skip', name); continue
    im = Image.open(p).convert('RGBA')
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    r, g, b, a = im.split()
    faded = ImageChops.multiply(a, edge_mask(*im.size))
    solid = a.point(lambda v: 255 if v >= 250 else 0)
    im = Image.merge('RGBA', (r, g, b, Image.composite(a, faded, solid)))
    out = os.path.join(DST, name + '.webp'); im.save(out, 'WEBP', quality=86, method=6)
    print(out, im.size, os.path.getsize(out) // 1024, 'KB')
