# -*- coding: utf-8 -*-
"""
Portada (cover) de la pagina publica de Notion — Sistemas Reales.

Pillow puro, 100% local, coste 0. Sin red, sin navegador, sin APIs.

MEDIDA
  1500 x 600 px. Notion recorta el cover por ancho y muestra una banda
  horizontal; la zona util real es la franja central vertical.
  El titulo y el icono de la pagina se pintan DEBAJO del cover (no encima),
  asi que no hay riesgo de solape, pero se deja aire abajo igualmente.

PALETA (la misma de las galerias de Gumroad y de los banners)
  navy #0a0e18 · cian #38bdf8 · ambar #fbbf24 · verde #34d399

CONTENIDO: solo hechos. Cero metricas, cero clientes, cero testimonios.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

OUT = Path(__file__).parent

BG    = (10, 14, 24)
CYAN  = (56, 189, 248)
AMBER = (251, 191, 36)
GREEN = (52, 211, 153)
WHITE = (255, 255, 255)
GRAY  = (148, 163, 184)
GRAY2 = (100, 116, 139)
LINE  = (34, 46, 70)

LS = "/usr/share/fonts/truetype/liberation/LiberationSans"

W, H = 1500, 600


def F(sz, bold=False):
    return ImageFont.truetype(f"{LS}-{'Bold' if bold else 'Regular'}.ttf", max(int(sz), 1))


def tw(d, s, f):
    return d.textlength(s, font=f)


def linea_mixta(d, x, y, trozos, f):
    cx = x
    for t, c in trozos:
        d.text((cx, y), t, font=f, fill=c)
        cx += tw(d, t, f)
    return cx - x


def fondo(img):
    """Navy con dos halos suaves (cian arriba-izq, ambar abajo-der) y rejilla tenue."""
    d = ImageDraw.Draw(img)

    halo = Image.new("RGB", (W, H), BG)
    hd = ImageDraw.Draw(halo)
    hd.ellipse([-260, -320, 760, 420], fill=(18, 38, 62))
    hd.ellipse([W - 620, H - 300, W + 240, H + 260], fill=(40, 32, 14))
    halo = halo.filter(ImageFilter.GaussianBlur(190))
    img.paste(Image.blend(img, halo, 0.85), (0, 0))

    d = ImageDraw.Draw(img)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(15, 21, 34), width=1)
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(15, 21, 34), width=1)


def barra_superior(d):
    d.rectangle([0, 0, W, 6], fill=CYAN)
    d.rectangle([0, 0, 420, 6], fill=AMBER)


def contenido(d):
    x = 110
    y = 132

    # Kicker
    fk = F(23, bold=True)
    linea_mixta(d, x, y, [
        ("SISTEMAS REALES", CYAN),
        ("   ·   ", GRAY2),
        ("n8n E IA LOCAL PARA HOSTELERÍA", GRAY),
    ], fk)
    y += 62

    # Titular en dos lineas
    ft = F(66, bold=True)
    d.text((x, y), "Food cost, mermas, APPCC", font=ft, fill=WHITE)
    y += 78
    linea_mixta(d, x, y, [("y facturas. ", WHITE), ("Automatizados.", AMBER)], ft)
    y += 96

    # Subtitulo
    fs = F(29)
    d.text((x, y), "Sin cuota mensual y sin que tus números salgan de tu local.",
           font=fs, fill=GRAY)
    y += 74

    # Hairline
    d.line([(x, y), (W - 110, y)], fill=LINE, width=2)
    y += 34

    # Tres sellos
    fp = F(25, bold=True)
    sellos = [("SIN IA EN LA NUBE", GREEN), ("SIN CLAVES", GREEN), ("SIN CUOTA", GREEN)]
    cx = x
    for i, (t, c) in enumerate(sellos):
        if i:
            d.text((cx, y), "   ·   ", font=fp, fill=GRAY2)
            cx += tw(d, "   ·   ", fp)
        d.text((cx, y), t, font=fp, fill=c)
        cx += tw(d, t, fp)

    # Credencial canonica (derecha, misma linea)
    fc = F(24)
    cred = "25 años en hostelería · 10 al frente de un mesón"
    d.text((W - 110 - tw(d, cred, fc), y + 1), cred, font=fc, fill=GRAY2)


def vinieta(img):
    v = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(v)
    vd.rectangle([0, int(H * 0.80), W, H], fill=70)
    v = v.filter(ImageFilter.GaussianBlur(60))
    img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), v)


def main():
    img = Image.new("RGB", (W, H), BG)
    fondo(img)
    vinieta(img)
    d = ImageDraw.Draw(img)
    barra_superior(d)
    contenido(d)
    OUT.mkdir(parents=True, exist_ok=True)
    ruta = OUT / "cover-notion-1500x600.png"
    img.save(ruta, "PNG")
    print("OK ->", ruta)


if __name__ == "__main__":
    main()
