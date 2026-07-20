# -*- coding: utf-8 -*-
"""
Portada (cover) de la pagina publica de Notion — Sistemas Reales.

Pillow puro, 100% local, coste 0. Sin red, sin navegador, sin APIs.

=============================================================================
DECISION DE DISENO — PORTADA SIN TEXTO  (2026-07-20, tras fallo verificado)
=============================================================================
La v1 llevaba titular + subtitulo + sellos. PUBLICADA SE VEIA MAL:
  - Notion NO muestra la imagen entera: recorta una FRANJA HORIZONTAL cuyo
    alto depende del ANCHO DE LA VENTANA. En pantalla ancha la franja es
    estrecha -> el titular salia cortado por arriba.
  - Notion encaja el ICONO de la pagina ENCIMA del cover, abajo a la
    izquierda -> se comia la primera letra de la linea de apoyo.

Como el recorte es variable, CUALQUIER texto en el cover es una apuesta que
se pierde en algun ancho. Por eso esta version es PURAMENTE GRAFICA:
  - Cero texto -> imposible que se corte mal a ningun ancho.
  - Composicion por BANDAS HORIZONTALES: cualquier franja que Notion recorte
    sigue siendo una imagen valida y equilibrada.
  - Esquina inferior izquierda deliberadamente lisa y oscura -> el icono de
    la pagina se apoya limpio encima.
El mensaje vive en el CUERPO de la pagina, que no se recorta nunca.

PALETA (la misma de las galerias de Gumroad y de los banners)
  navy #0a0e18 · cian #38bdf8 · ambar #fbbf24 · verde #34d399
"""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

OUT = Path(__file__).parent

BG    = (10, 14, 24)
CYAN  = (56, 189, 248)
AMBER = (251, 191, 36)
GREEN = (52, 211, 153)

W, H = 1500, 600


def fondo(img):
    """Navy con halos suaves. Horizontalmente variado, verticalmente estable:
    asi cualquier franja recortada sigue teniendo la misma riqueza."""
    halo = Image.new("RGB", (W, H), BG)
    hd = ImageDraw.Draw(halo)
    # Halo cian: columna izquierda, alto completo -> sobrevive a cualquier recorte
    hd.ellipse([-420, -520, 720, H + 520], fill=(16, 42, 70))
    # Halo ambar: columna derecha
    hd.ellipse([W - 560, -460, W + 380, H + 460], fill=(46, 36, 14))
    # Halo verde muy tenue al centro, para que no quede un hueco muerto
    hd.ellipse([560, -300, 1060, H + 300], fill=(12, 34, 30))
    halo = halo.filter(ImageFilter.GaussianBlur(210))
    img.paste(Image.blend(img, halo, 0.9), (0, 0))


def rejilla(img):
    """Rejilla tecnica muy tenue: da textura sin competir con nada."""
    d = ImageDraw.Draw(img)
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=(16, 22, 36), width=1)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(16, 22, 36), width=1)


def columnas(img):
    """Columnas VERTICALES de altura completa, tipo grafico de control.

    Clave del diseno: al ser verticales y llegar de borde a borde, CUALQUIER
    franja horizontal que Notion recorte contiene exactamente la misma
    composicion. El recorte deja de ser un riesgo.

    Ritmo: anchos y opacidades variables (evoca una serie de datos, que es de
    lo que va el negocio) sin representar ninguna cifra concreta -> no afirma
    ninguna metrica.
    """
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    # (x, ancho, color, alpha) — patron irregular pero equilibrado
    serie = [
        (150, 26, CYAN, 26), (196, 14, CYAN, 16), (226, 34, CYAN, 40),
        (280, 18, CYAN, 20), (312, 10, GREEN, 22), (338, 44, CYAN, 30),
        (400, 16, CYAN, 14), (432, 28, GREEN, 26), (478, 12, CYAN, 18),
        (508, 38, CYAN, 34), (564, 20, GREEN, 20), (600, 14, CYAN, 15),
        (700, 30, AMBER, 22), (748, 16, AMBER, 14), (782, 46, AMBER, 32),
        (846, 18, AMBER, 18), (882, 12, GREEN, 16), (912, 36, AMBER, 26),
        (966, 22, AMBER, 16), (1006, 14, AMBER, 20), (1038, 40, AMBER, 30),
        (1096, 18, AMBER, 15), (1132, 26, GREEN, 18), (1176, 12, AMBER, 22),
        (1206, 34, AMBER, 26), (1258, 16, AMBER, 14), (1292, 24, AMBER, 20),
        (1334, 12, GREEN, 15), (1364, 30, AMBER, 24),
    ]
    for x, w, col, a in serie:
        d.rectangle([x, 0, x + w, H], fill=(*col, a))

    img.paste(Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB"), (0, 0))

    d = ImageDraw.Draw(img)
    # Filetes de borde: rematan la pieza sin depender de que se vean
    d.rectangle([0, 0, 380, 5], fill=AMBER)
    d.rectangle([380, 0, 980, 5], fill=CYAN)
    d.rectangle([980, 0, W, 5], fill=GREEN)
    d.rectangle([0, H - 5, W, H], fill=(22, 32, 50))


def zona_icono(img):
    """Notion apoya el icono de la pagina abajo a la izquierda.
    Se oscurece y se limpia esa esquina para que el icono se lea siempre."""
    m = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(m)
    md.ellipse([-160, H - 300, 460, H + 200], fill=120)
    m = m.filter(ImageFilter.GaussianBlur(90))
    img.paste(Image.new("RGB", (W, H), (4, 7, 13)), (0, 0), m)


def main():
    img = Image.new("RGB", (W, H), BG)
    fondo(img)
    rejilla(img)
    columnas(img)
    zona_icono(img)
    OUT.mkdir(parents=True, exist_ok=True)
    ruta = OUT / "cover-notion-1500x600.png"
    img.save(ruta, "PNG")
    print("OK ->", ruta)

    # Simulacion de los recortes de Notion, para verificar ANTES de publicar.
    # Notion muestra una franja centrada cuyo alto varia con el ancho de ventana.
    pruebas = {"ancho": 0.42, "medio": 0.62, "estrecho": 0.90}
    for nombre, frac in pruebas.items():
        alto = int(H * frac)
        top = (H - alto) // 2
        img.crop((0, top, W, top + alto)).save(OUT / f"_recorte-simulado-{nombre}.png")
    print("OK -> recortes simulados (ancho / medio / estrecho)")


if __name__ == "__main__":
    main()
