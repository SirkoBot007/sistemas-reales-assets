# -*- coding: utf-8 -*-
"""
Banner de portada para LinkedIn — Sistemas Reales / Alberto (Sirko007).
1584x396 PNG. Pillow puro, local, cero coste.

ZONA SEGURA (LinkedIn):
  - La foto de perfil circular tapa la esquina INFERIOR IZQUIERDA -> nada util
    en los primeros ~350 px de ancho.
  - En movil se recortan los bordes -> margen de 70 px arriba/abajo/derecha.
  - Todo el contenido relevante vive en x >= 400 y dentro de y 55..340.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1584, 396
SAFE_X = 400          # a partir de aqui puede ir texto importante
MARGIN_R = 96

# --- Paleta Sistemas Reales (misma que las galerias de Gumroad) ---
BG      = (10, 14, 24)
CYAN    = (56, 189, 248)
AMBER   = (251, 191, 36)
GREEN   = (52, 211, 153)
WHITE   = (255, 255, 255)
GRAY    = (148, 163, 184)
GRAY2   = (100, 116, 139)
LINE    = (40, 54, 80)
CARD    = (17, 24, 38)
CARD_B  = (38, 52, 78)

LS = "/usr/share/fonts/truetype/liberation/LiberationSans"
DJ = "/usr/share/fonts/truetype/dejavu/DejaVu"

def F(sz, bold=False):
    return ImageFont.truetype(f"{LS}-{'Bold' if bold else 'Regular'}.ttf", int(sz))

def FD(sz, bold=False):
    return ImageFont.truetype(f"{DJ}Sans{'-Bold' if bold else ''}.ttf", int(sz))

def tw(d, s, f):
    return d.textlength(s, font=f)

OUT = Path(__file__).parent


def fondo(warm_right=False):
    """Navy profundo + dos halos difuminados (cian a la derecha, ambar sutil)."""
    img = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG)
    g = ImageDraw.Draw(glow)
    g.ellipse([980, -300, 1900, 470], fill=(18, 48, 74))         # halo cian dcha
    if warm_right:
        g.ellipse([1180, 120, 1760, 620], fill=(52, 34, 16))     # calido inferior dcha
    g.ellipse([-380, 60, 380, 620], fill=(16, 24, 40))           # relleno izq (bajo la foto)
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(170)), 0.92)
    return img


def rejilla(d):
    """Rejilla tecnica MUY sutil, solo en la mitad derecha. Da textura sin ruido."""
    for x in range(SAFE_X, W, 44):
        d.line([x, 0, x, H], fill=(15, 21, 33), width=1)
    for y in range(0, H, 44):
        d.line([SAFE_X, y, W, y], fill=(15, 21, 33), width=1)


def barra_acento(d, x, y, h, color=CYAN, w=5):
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=color)


def pill(d, x, y, texto, color, f=None, pad_x=15, pad_y=9):
    f = f or F(15, True)
    a = tw(d, texto, f)
    d.rounded_rectangle([x, y, x + a + pad_x * 2, y + f.size + pad_y * 2],
                        radius=(f.size + pad_y * 2) // 2,
                        fill=(color[0] // 9, color[1] // 9, color[2] // 9),
                        outline=(color[0] // 3, color[1] // 3, color[2] // 3), width=1)
    d.text((x + pad_x, y + pad_y), texto, font=f, fill=color)
    return x + a + pad_x * 2


def linea_mixta(d, x, y, trozos, f):
    """Dibuja una linea con tramos de distinto color. Devuelve el ancho total."""
    cx = x
    for t, c in trozos:
        d.text((cx, y), t, font=f, fill=c)
        cx += tw(d, t, f)
    return cx - x


def ancho_mixta(d, trozos, f):
    return sum(tw(d, t, f) for t, _ in trozos)


# ══════════════════════════════════════════════════════════════════
# V1 — LA HISTORIA (el gancho: hostelero que automatiza hosteleria)
# ══════════════════════════════════════════════════════════════════
def v1():
    img = fondo(warm_right=True)
    d = ImageDraw.Draw(img)
    rejilla(d)

    x = SAFE_X + 40
    barra_acento(d, x - 28, 108, 130, AMBER)

    d.text((x, 68), "ALBERTO  ·  SISTEMAS REALES  ·  MÁS DE 25 AÑOS EN HOSTELERÍA",
           font=F(16, True), fill=CYAN)

    fh = F(48, True)
    linea_mixta(d, x, 110, [("Los últimos 10, al frente de un mesón.", WHITE)], fh)
    linea_mixta(d, x, 172, [("Ahora ", WHITE), ("automatizo el de otros", AMBER),
                            (".", WHITE)], fh)

    d.text((x, 254), "Food cost · Mermas y barriles · Registros de APPCC · Facturación con IA local",
           font=F(19), fill=GRAY)

    # cierre abajo, misma columna: sin cuotas / sin nubes
    fc = F(17, True)
    d.text((x, 300), "Sin cuotas mensuales   ·   Sin depender de nubes ajenas",
           font=fc, fill=GREEN)
    img.save(OUT / "banner-v1.png")
    print("v1 ok")


# ══════════════════════════════════════════════════════════════════
# V2 — LOS SERVICIOS (que hago, en 4 tarjetas)
# ══════════════════════════════════════════════════════════════════
def v2():
    img = fondo()
    d = ImageDraw.Draw(img)
    rejilla(d)

    x = SAFE_X + 36
    d.text((x, 58), "ALBERTO  ·  SISTEMAS REALES  ·  MÁS DE 25 AÑOS EN HOSTELERÍA",
           font=F(15, True), fill=CYAN)

    fh = F(40, True)
    linea_mixta(d, x, 90, [("Automatizo la operativa de ", WHITE), ("bares", CYAN)], fh)
    linea_mixta(d, x, 138, [("y ", WHITE), ("restaurantes", CYAN),
                            (" — 10 años en un mesón.", WHITE)], fh)

    # 4 tarjetas
    cards = [
        ("FOOD COST", "qué te cuesta cada plato", CYAN),
        ("MERMAS Y BARRILES", "los euros que se van", AMBER),
        ("REGISTROS APPCC", "la hoja que pide sanidad", GREEN),
        ("FACTURAS CON IA", "leídas en tu ordenador", CYAN),
    ]
    total_w = W - MARGIN_R - x
    gap = 16
    cw = (total_w - gap * 3) / 4
    cy, ch = 208, 84
    for i, (k, v, c) in enumerate(cards):
        cx = x + i * (cw + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=12,
                            fill=CARD, outline=CARD_B, width=1)
        d.rounded_rectangle([cx, cy + 14, cx + 4, cy + ch - 14], radius=2, fill=c)
        d.text((cx + 18, cy + 20), k, font=F(16, True), fill=WHITE)
        d.text((cx + 18, cy + 46), v, font=F(14), fill=GRAY2)

    fc = F(16, True)
    cierre = "Sin cuotas mensuales  ·  Sin depender de nubes ajenas"
    d.text((x, 328), cierre, font=fc, fill=GREEN)
    img.save(OUT / "banner-v2.png")
    print("v2 ok")


# ══════════════════════════════════════════════════════════════════
# V3 — MINIMALISTA (una sola frase, mucho aire, centrado)
# ══════════════════════════════════════════════════════════════════
def v3():
    img = fondo()
    d = ImageDraw.Draw(img)

    # centro del bloque util (evitando la foto de perfil)
    cx = SAFE_X + (W - MARGIN_R - SAFE_X) / 2

    f_kick = F(16, True)
    k = "25 AÑOS EN HOSTELERÍA   ·   LOS ÚLTIMOS 10 AL FRENTE DE UN MESÓN"
    d.text((cx - tw(d, k, f_kick) / 2, 84), k, font=f_kick, fill=CYAN)

    fh = F(50, True)
    l1 = [("De la barra ", WHITE), ("al sistema.", CYAN)]
    d.text((cx - ancho_mixta(d, l1, fh) / 2, 134), "", font=fh)
    linea_mixta(d, cx - ancho_mixta(d, l1, fh) / 2, 134, l1, fh)

    fs = F(21)
    s = "Food cost, mermas, barriles, APPCC y facturas — automatizado para hostelería."
    d.text((cx - tw(d, s, fs) / 2, 208), s, font=fs, fill=GRAY)

    # regla fina con nudo central
    ry = 262
    d.line([cx - 300, ry, cx - 14, ry], fill=LINE, width=1)
    d.line([cx + 14, ry, cx + 300, ry], fill=LINE, width=1)
    d.ellipse([cx - 4, ry - 4, cx + 4, ry + 4], fill=CYAN)

    fc = F(17, True)
    c = "Sin cuotas mensuales   ·   Sin depender de nubes ajenas"
    d.text((cx - tw(d, c, fc) / 2, 288), c, font=fc, fill=GREEN)

    img.save(OUT / "banner-v3.png")
    print("v3 ok")


if __name__ == "__main__":
    v1(); v2(); v3()
