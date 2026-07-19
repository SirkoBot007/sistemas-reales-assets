# -*- coding: utf-8 -*-
"""
Portada / banner de la TIENDA DE GUMROAD — Sistemas Reales (sistemasreales.gumroad.com).

Pillow puro, 100% local, coste 0. Sin red, sin navegador, sin APIs.

MEDIDA
  Principal : 1600 x 400 px  (ratio 4:1)
  Alternativa: 1280 x 320 px  (mismo ratio, por si Gumroad recorta distinto)
  Nota: la medida NO se pudo verificar en la doc oficial en esta sesion (sin
  navegador por peticion de Alberto). 1600x400 es la medida de trabajo; el
  ratio 4:1 es lo que de verdad importa porque Gumroad reencuadra por ancho.

ZONA SEGURA (Gumroad superpone avatar + nombre de la tienda sobre la cabecera)
  - Nada critico en la BANDA INFERIOR (ultimo 28 % de alto) -> ahi cae el
    avatar circular y el nombre de la tienda.
  - Margenes laterales generosos: el navegador recorta por ancho en movil.
  - Todo el texto util vive dentro de y = 0.14*H .. 0.68*H.

PALETA (la misma de las galerias de Gumroad y del banner de LinkedIn)
  navy #0a0e18 · cian #38bdf8 · ambar #fbbf24 · verde #34d399

CONTENIDO: solo hechos. Cero metricas, cero clientes, cero testimonios.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

OUT = Path(__file__).parent

# --- Paleta Sistemas Reales ---
BG     = (10, 14, 24)
CYAN   = (56, 189, 248)
AMBER  = (251, 191, 36)
GREEN  = (52, 211, 153)
WHITE  = (255, 255, 255)
GRAY   = (148, 163, 184)
GRAY2  = (100, 116, 139)
LINE   = (34, 46, 70)

LS = "/usr/share/fonts/truetype/liberation/LiberationSans"

TAMANOS = [(1600, 400), (1280, 320)]


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


def ancho_mixta(d, trozos, f):
    return sum(tw(d, t, f) for t, _ in trozos)


def fondo(W, H, calido=True):
    """Navy profundo + halos difuminados. Degradado suave, nada de ruido."""
    img = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG)
    g = ImageDraw.Draw(glow)
    # halo cian arriba-derecha
    g.ellipse([W * 0.58, -H * 0.85, W * 1.22, H * 1.12], fill=(17, 46, 72))
    if calido:
        # halo ambar muy sutil, abajo-derecha
        g.ellipse([W * 0.74, H * 0.30, W * 1.10, H * 1.55], fill=(48, 32, 15))
    # relleno frio a la izquierda para que no quede plano
    g.ellipse([-W * 0.24, -H * 0.35, W * 0.34, H * 1.35], fill=(14, 21, 36))
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(int(W * 0.105))), 0.94)
    return img


def rejilla(d, W, H, paso, desde=0.0):
    """Rejilla tecnica casi invisible: da textura de 'sistema' sin ensuciar."""
    x0 = int(W * desde)
    for x in range(x0, W, paso):
        d.line([x, 0, x, H], fill=(15, 21, 34), width=1)
    for y in range(0, H, paso):
        d.line([x0, y, W, y], fill=(15, 21, 34), width=1)


def vineta_inferior(img, W, H):
    """Oscurece MUY suavemente la banda de abajo: ahi Gumroad pone avatar+nombre.
    Asi el overlay se lee siempre bien y ademas da sensacion de profundidad."""
    capa = Image.new("L", (W, H), 0)
    dd = ImageDraw.Draw(capa)
    banda = int(H * 0.42)
    for i in range(banda):
        y = H - banda + i
        dd.line([0, y, W, y], fill=int(120 * (i / banda) ** 2))
    negro = Image.new("RGB", (W, H), (5, 8, 15))
    return Image.composite(negro, img, capa.filter(ImageFilter.GaussianBlur(int(H * 0.05))))


def barra(d, x, y, h, color, w):
    d.rounded_rectangle([x, y, x + w, y + h], radius=max(w // 2, 1), fill=color)


# ══════════════════════════════════════════════════════════════════════════
# V1 — LA MARCA (nombre grande + lo que resuelve + criterio). Sobria.
# ══════════════════════════════════════════════════════════════════════════
def v1(W, H):
    S = W / 1600
    img = fondo(W, H, calido=True)
    d = ImageDraw.Draw(img)
    rejilla(d, W, H, int(48 * S), desde=0.0)   # rejilla completa: sin corte visible

    x = int(96 * S)
    barra(d, x, int(92 * S), int(126 * S), CYAN, int(5 * S))
    xt = x + int(30 * S)

    d.text((xt, int(88 * S)), "AUTOMATIZACIÓN PARA HOSTELERÍA Y PYMES",
           font=F(17 * S, True), fill=CYAN)

    fh = F(62 * S, True)
    linea_mixta(d, xt, int(120 * S), [("Sistemas ", WHITE), ("Reales", CYAN)], fh)

    d.text((xt, int(206 * S)),
           "Food cost  ·  Mermas y barriles  ·  Registros de APPCC  ·  Facturación con IA local",
           font=F(21 * S), fill=GRAY)

    fc = F(18 * S, True)
    d.text((xt, int(246 * S)), "Sin cuotas mensuales   ·   Sin depender de nubes ajenas",
           font=fc, fill=GREEN)

    # --- columna derecha: equilibra el peso sin recargar (hechos, no metricas) ---
    xr = W - int(96 * S)
    fr_k = F(14 * S, True)
    fr_v = F(17 * S, True)
    filas = [("HECHO POR", "quien estuvo 10 años al frente de un mesón"),
             ("FUNCIONA EN", "tu ordenador — n8n e IA local"),
             ("SE PAGA", "una vez, no cada mes")]
    yr = int(96 * S)
    d.line([xr - int(430 * S), yr - int(10 * S), xr, yr - int(10 * S)], fill=LINE, width=1)
    for k, v in filas:
        d.text((xr - tw(d, k, fr_k), yr + int(4 * S)), k, font=fr_k, fill=GRAY2)
        d.text((xr - tw(d, v, fr_v), yr + int(24 * S)), v, font=fr_v, fill=GRAY)
        yr += int(58 * S)
        d.line([xr - int(430 * S), yr - int(10 * S), xr, yr - int(10 * S)], fill=LINE, width=1)

    img = vineta_inferior(img, W, H)
    return img


# ══════════════════════════════════════════════════════════════════════════
# V2 — LO QUE VENDO (nombre + 4 columnas separadas por hairlines). Editorial.
# ══════════════════════════════════════════════════════════════════════════
def v2(W, H):
    S = W / 1600
    img = fondo(W, H, calido=False)
    d = ImageDraw.Draw(img)
    rejilla(d, W, H, int(48 * S), desde=0.0)

    x = int(96 * S)
    d.text((x, int(58 * S)), "SISTEMAS REALES", font=F(16 * S, True), fill=CYAN)
    # criterio, alineado a la derecha en la misma linea del kicker
    fcr = F(16 * S, True)
    cr = "Sin cuotas mensuales   ·   Sin depender de nubes ajenas"
    d.text((W - int(96 * S) - tw(d, cr, fcr), int(58 * S)), cr, font=fcr, fill=GREEN)

    fh = F(48 * S, True)
    linea_mixta(d, x, int(94 * S),
                [("Automatizo la operativa de ", WHITE), ("bares, restaurantes", CYAN)], fh)
    linea_mixta(d, x, int(146 * S), [("y pequeños negocios.", WHITE)], fh)

    # 4 columnas con separadores finos — más sobrio que las tarjetas
    cols = [
        ("FOOD COST", "qué te cuesta cada plato", CYAN),
        ("MERMAS Y BARRILES", "los euros que se van", AMBER),
        ("REGISTROS APPCC", "la hoja que pide sanidad", GREEN),
        ("FACTURAS CON IA", "leídas en tu ordenador", CYAN),
    ]
    y0 = int(212 * S)
    alto = int(58 * S)
    util = W - x - int(96 * S)
    cw = util / 4
    for i, (k, v, c) in enumerate(cols):
        cx = x + i * cw
        if i:
            d.line([cx - int(20 * S), y0 + int(4 * S), cx - int(20 * S), y0 + alto],
                   fill=LINE, width=1)
        d.rounded_rectangle([cx, y0, cx + int(22 * S), y0 + int(3 * S)],
                            radius=int(2 * S), fill=c)
        d.text((cx, y0 + int(16 * S)), k, font=F(15 * S, True), fill=WHITE)
        d.text((cx, y0 + int(38 * S)), v, font=F(14 * S), fill=GRAY)

    img = vineta_inferior(img, W, H)
    return img


# ══════════════════════════════════════════════════════════════════════════
# V3 — MINIMALISTA CENTRADO (mucho aire, una sola idea). El más elegante.
# ══════════════════════════════════════════════════════════════════════════
def v3(W, H):
    S = W / 1600
    img = fondo(W, H, calido=True)
    d = ImageDraw.Draw(img)
    cx = W / 2

    fk = F(16 * S, True)
    k = "AUTOMATIZACIÓN PARA HOSTELERÍA Y PYMES"
    d.text((cx - tw(d, k, fk) / 2, int(74 * S)), k, font=fk, fill=CYAN)

    fh = F(64 * S, True)
    t = [("Sistemas ", WHITE), ("Reales", CYAN)]
    d.text((cx - ancho_mixta(d, t, fh) / 2, int(0)), "", font=fh)
    linea_mixta(d, cx - ancho_mixta(d, t, fh) / 2, int(106 * S), t, fh)

    fs = F(20 * S)
    s = "Food cost · mermas · barriles · APPCC · facturación con IA local"
    d.text((cx - tw(d, s, fs) / 2, int(192 * S)), s, font=fs, fill=GRAY)

    # regla fina con nudo central
    ry = int(234 * S)
    d.line([cx - int(330 * S), ry, cx - int(15 * S), ry], fill=LINE, width=1)
    d.line([cx + int(15 * S), ry, cx + int(330 * S), ry], fill=LINE, width=1)
    r = max(int(4 * S), 2)
    d.ellipse([cx - r, ry - r, cx + r, ry + r], fill=AMBER)

    fc = F(17 * S, True)
    c = "Sin cuotas mensuales   ·   Sin depender de nubes ajenas"
    d.text((cx - tw(d, c, fc) / 2, int(256 * S)), c, font=fc, fill=GREEN)

    img = vineta_inferior(img, W, H)
    return img


if __name__ == "__main__":
    for nombre, fn in (("v1", v1), ("v2", v2), ("v3", v3)):
        for W, H in TAMANOS:
            sufijo = "" if (W, H) == (1600, 400) else f"-{W}x{H}"
            ruta = OUT / f"banner-{nombre}{sufijo}.png"
            fn(W, H).save(ruta)
            print("ok", ruta.name)
