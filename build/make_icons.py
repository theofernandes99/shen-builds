# Redessine les icônes de l'appli (app/icons) : lame spirituelle cyan sur fond crépuscule, anneau doré.
import os
from PIL import Image, ImageDraw, ImageFilter
ICONS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'icons')
S = 1024
def make(scale=1.0, rounded=True):
    bg = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    base = Image.new('RGBA', (S, S), (10, 14, 28, 255))
    # lueur crépuscule
    glow = Image.new('RGBA', (S, S), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse((S*.18, S*.16, S*.82, S*.86), fill=(60, 70, 160, 150))
    base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(120)))
    c = S / 2
    def sc(v): return c + (v - c) * scale
    # anneau doré
    ring = Image.new('RGBA', (S, S), (0, 0, 0, 0)); r = ImageDraw.Draw(ring)
    R = 300 * scale
    r.ellipse((c-R, c-R, c+R, c+R), outline=(207, 174, 103, 255), width=int(26*scale))
    base = Image.alpha_composite(base, ring)
    # lame (polygone) avec halo
    blade = [(c, sc(150)), (sc(c+62), sc(330)), (sc(c+40), sc(700)), (c, sc(850)), (sc(c-40), sc(700)), (sc(c-62), sc(330))]
    halo = Image.new('RGBA', (S, S), (0, 0, 0, 0)); h = ImageDraw.Draw(halo)
    h.polygon(blade, fill=(114, 212, 255, 230))
    base = Image.alpha_composite(base, halo.filter(ImageFilter.GaussianBlur(40)))
    sharp = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(sharp)
    d.polygon(blade, fill=(150, 225, 255, 255))
    inner = [(c, sc(210)), (sc(c+22), sc(340)), (sc(c+14), sc(690)), (c, sc(790)), (sc(c-14), sc(690)), (sc(c-22), sc(340))]
    d.polygon(inner, fill=(235, 250, 255, 255))
    # garde de la lame
    d.rounded_rectangle((sc(c-120), sc(640), sc(c+120), sc(672)), radius=int(14*scale), fill=(207, 174, 103, 255))
    base = Image.alpha_composite(base, sharp)
    if rounded:
        m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, S, S), radius=int(S*.22), fill=255)
        bg.paste(base, (0, 0), m); return bg
    return base
std = make(1.0, rounded=False)   # iOS arrondit lui-même ; fond plein
mask = make(0.78, rounded=False) # zone sûre des icônes « maskable »
for n, im in [('icon-192.png', std.resize((192,192), Image.LANCZOS)), ('icon-512.png', std.resize((512,512), Image.LANCZOS)),
              ('icon-maskable-512.png', mask.resize((512,512), Image.LANCZOS)), ('apple-touch-icon.png', std.convert('RGB').resize((180,180), Image.LANCZOS))]:
    im.save(os.path.join(ICONS, n), optimize=True)
make(1.0, rounded=True).resize((64,64), Image.LANCZOS).save(os.path.join(ICONS, 'favicon.png'), optimize=True)

print('ok')
