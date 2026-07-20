# -*- coding: utf-8 -*-
"""
Banners LinkedIn v2 — CREDENCIAL COMPLETA.
"Mas de 25 anos en hosteleria. Los ultimos 10, al frente de un meson."
Reutiliza el diseno ganador (v1): navy + rejilla + barra ambar + cierre verde.
Todo el ancho se MIDE con textlength() y se auto-reduce si no cabe.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1584, 396
SAFE_X = 400
MARGIN_R = 96
MAX_X = W - MARGIN_R

BG=(10,14,24); CYAN=(56,189,248); AMBER=(251,191,36); GREEN=(52,211,153)
WHITE=(255,255,255); GRAY=(148,163,184); LINE=(40,54,80)

LS = "/usr/share/fonts/truetype/liberation/LiberationSans"
def F(sz, bold=False):
    return ImageFont.truetype(f"{LS}-{'Bold' if bold else 'Regular'}.ttf", int(sz))

OUT = Path(__file__).parent
AVISOS = []

def fondo(warm=True):
    img = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG)
    g = ImageDraw.Draw(glow)
    g.ellipse([980, -300, 1900, 470], fill=(18, 48, 74))
    if warm:
        g.ellipse([1180, 120, 1760, 620], fill=(52, 34, 16))
    g.ellipse([-380, 60, 380, 620], fill=(16, 24, 40))
    return Image.blend(img, glow.filter(ImageFilter.GaussianBlur(170)), 0.92)

def rejilla(d, x0=SAFE_X):
    for x in range(x0, W, 44):
        d.line([x, 0, x, H], fill=(15, 21, 33), width=1)
    for y in range(0, H, 44):
        d.line([x0, y, W, y], fill=(15, 21, 33), width=1)

def ancho(d, trozos, f):
    return sum(d.textlength(t, font=f) for t, _ in trozos)

def fit(d, trozos, size, bold=True, x=SAFE_X+40, limite=MAX_X, minimo=13):
    """Reduce el tamano hasta que la linea COMPLETA cabe. Medido, no estimado."""
    s = size
    while s > minimo:
        f = F(s, bold)
        if x + ancho(d, trozos, f) <= limite:
            return f
        s -= 1
    return F(minimo, bold)

def pinta(d, x, y, trozos, f, etiqueta=""):
    cx = x
    for t, c in trozos:
        d.text((cx, y), t, font=f, fill=c)
        cx += d.textlength(t, font=f)
    if cx > MAX_X:
        AVISOS.append(f"DESBORDA {etiqueta}: {cx:.0f} > {MAX_X}")
    return cx

def barra(d, x, y, h, color=AMBER, w=5):
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=color)

SERV = "Food cost · Mermas y barriles · Registros de APPCC · Facturación con IA local"
CIERRE = "Sin cuotas mensuales   ·   Sin depender de nubes ajenas"

# ═════════ A — CREDENCIAL COMPLETA COMO TITULAR (2 lineas grandes) ═════════
def A():
    img = fondo(); d = ImageDraw.Draw(img); rejilla(d)
    x = SAFE_X + 40
    d.text((x, 48), "ALBERTO  ·  SISTEMAS REALES", font=F(16, True), fill=CYAN)

    l1 = [("Más de 25 años en hostelería.", WHITE)]
    l2 = [("Los últimos 10, ", WHITE), ("al frente de un mesón", AMBER), (".", WHITE)]
    f = fit(d, l2, 42, x=x)
    f = min(f.size, fit(d, l1, 42, x=x).size)
    f = F(f, True)
    barra(d, x - 28, 86, 118, AMBER)
    pinta(d, x, 86, l1, f, "A-l1")
    pinta(d, x, 86 + f.size + 12, l2, f, "A-l2")

    fg = fit(d, [("Ahora automatizo el de otros.", CYAN)], 27, x=x)
    pinta(d, x, 212, [("Ahora ", GRAY), ("automatizo el de otros", CYAN), (".", GRAY)], fg, "A-gancho")

    fs = fit(d, [(SERV, GRAY)], 18, bold=False, x=x)
    pinta(d, x, 268, [(SERV, GRAY)], fs, "A-serv")
    fc = fit(d, [(CIERRE, GREEN)], 17, x=x)
    pinta(d, x, 310, [(CIERRE, GREEN)], fc, "A-cierre")
    img.save(OUT / "banner-linkedin-A.png"); print("A ok")

# ═════════ B — CREDENCIAL ARRIBA EN CIAN, GANCHO GIGANTE ═════════
def B():
    img = fondo(); d = ImageDraw.Draw(img); rejilla(d)
    x = SAFE_X + 40
    kick = [("MÁS DE 25 AÑOS EN HOSTELERÍA   ·   LOS ÚLTIMOS 10, AL FRENTE DE UN MESÓN", CYAN)]
    fk = fit(d, kick, 19, x=x)
    pinta(d, x, 96, kick, fk, "B-kicker")

    barra(d, x - 28, 142, 108, AMBER)
    l1 = [("Ahora ", WHITE), ("automatizo el de otros", AMBER), (".", WHITE)]
    fh = fit(d, l1, 52, x=x)
    pinta(d, x, 142, l1, fh, "B-h1")

    fs = fit(d, [(SERV, GRAY)], 19, bold=False, x=x)
    pinta(d, x, 232, [(SERV, GRAY)], fs, "B-serv")

    d.line([x, 276, MAX_X - 40, 276], fill=LINE, width=1)
    fc = fit(d, [(CIERRE, GREEN)], 17, x=x)
    pinta(d, x, 300, [(CIERRE, GREEN)], fc, "B-cierre")
    img.save(OUT / "banner-linkedin-B.png"); print("B ok")

# ═════════ C — DOS COLUMNAS: CIFRAS A LA IZQUIERDA, MENSAJE A LA DERECHA ═════════
def C():
    img = fondo(); d = ImageDraw.Draw(img); rejilla(d)
    x = SAFE_X + 36
    COL = 300                     # ancho columna cifras
    xr = x + COL + 56             # arranque columna derecha

    # --- columna cifras ---
    d.line([xr - 30, 92, xr - 30, 306], fill=LINE, width=1)
    f25 = F(58, True); f10 = F(58, True); flab = F(15, True); fsub = F(16)
    barra(d, x - 24, 100, 74, CYAN)
    d.text((x, 96), "+25", font=f25, fill=CYAN)
    d.text((x + d.textlength("+25", font=f25) + 12, 128), "AÑOS", font=flab, fill=GRAY)
    d.text((x, 166), "en hostelería", font=fsub, fill=GRAY)

    barra(d, x - 24, 208, 74, AMBER)
    d.text((x, 204), "10", font=f10, fill=AMBER)
    d.text((x + d.textlength("10", font=f10) + 12, 236), "ÚLTIMOS", font=flab, fill=GRAY)
    d.text((x, 274), "al frente de un mesón", font=fsub, fill=GRAY)

    lim_izq = max(x + d.textlength("al frente de un mesón", font=fsub),
                  x + d.textlength("en hostelería", font=fsub))
    if lim_izq > xr - 40:
        AVISOS.append(f"C: columna izq invade la derecha ({lim_izq:.0f} > {xr-40})")

    # --- columna mensaje ---
    l1 = [("De la barra ", WHITE), ("al sistema", CYAN), (".", WHITE)]
    fh = fit(d, l1, 46, x=xr)
    pinta(d, xr, 104, l1, fh, "C-h1")
    fg = fit(d, [("Ahora automatizo el de otros.", AMBER)], 26, x=xr)
    pinta(d, xr, 168, [("Ahora ", WHITE), ("automatizo el de otros", AMBER), (".", WHITE)], fg, "C-gancho")

    serv_c = "Food cost · Mermas y barriles · APPCC · Facturación con IA local"
    fs = fit(d, [(serv_c, GRAY)], 18, bold=False, x=xr)
    pinta(d, xr, 224, [(serv_c, GRAY)], fs, "C-serv")
    fc = fit(d, [(CIERRE, GREEN)], 17, x=xr)
    pinta(d, xr, 278, [(CIERRE, GREEN)], fc, "C-cierre")
    img.save(OUT / "banner-linkedin-C.png"); print("C ok")

if __name__ == "__main__":
    A(); B(); C()
    print("AVISOS:", AVISOS if AVISOS else "ninguno — todo dentro de la zona segura")
