# Portada de la tienda de Gumroad — Sistemas Reales

Banner de cabecera para `sistemasreales.gumroad.com`. Generado en local con Pillow
(`_generador_banner_gumroad.py`), **coste 0**, sin red ni navegador.

## Ficheros

| Fichero | Medida | Qué es |
|---|---|---|
| `banner-v1.png` | 1600×400 | **RECOMENDADA** — la marca + lo que resuelve + columna de credenciales |
| `banner-v2.png` | 1600×400 | Editorial — los 4 servicios en columnas con hairlines |
| `banner-v3.png` | 1600×400 | Minimalista centrada — mucho aire, una sola idea |
| `banner-v*-1280x320.png` | 1280×320 | Mismas tres, mismo ratio 4:1, por si Gumroad recorta distinto |

## Medida — ⚠️ sin verificar en doc oficial

**1600 × 400 px (ratio 4:1)** es la medida de trabajo. **No se pudo confirmar en la
documentación oficial de Gumroad** en la sesión del 2026-07-19 porque Alberto pidió
expresamente no usar el navegador (estaba ocupado con otra tarea).
Lo que de verdad manda es el **ratio 4:1**: Gumroad reencuadra por ancho. Por eso se
entrega también la variante 1280×320.

> Pendiente: verificar la medida oficial cuando el navegador esté libre y, si difiere,
> regenerar (el script es paramétrico — basta tocar `TAMANOS`).

## Zona segura

Gumroad **superpone el avatar y el nombre de la tienda** sobre la cabecera.
Por eso, en las tres variantes:

- Todo el texto útil vive entre **y = 14 % y y = 68 %** del alto.
- El **28 % inferior queda libre** de texto crítico y además lleva una viñeta muy
  suave que oscurece la banda → el nombre que Gumroad pinta encima se lee siempre.
- Márgenes laterales de 96 px (a 1600 de ancho) por el recorte en móvil.

## Paleta

La misma de las galerías de producto y del banner de LinkedIn:
navy `#0a0e18` · cian `#38bdf8` · ámbar `#fbbf24` · verde `#34d399`.
Tipografía Liberation Sans (métricas de Arial/Helvetica).

## Contenido — solo hechos

Cero métricas, cero clientes, cero testimonios. Lo único factual afirmado es la
**credencial canónica** — **"25 años en hostelería · 10 al frente de un mesón"**
(variante corta, la que cabe en la columna derecha).

> 🔒 **No se reformula.** Fórmula larga fijada por Alberto el 2026-07-19:
> **«Más de 25 años en hostelería. Los últimos 10, al frente de un mesón.»**
> Las dos cifras son ciertas —25 = oficio desde 1999 en muchos locales; 10 = al
> mando de este mesón, 2015–2025— y **van siempre juntas**. Fuente Única:
> `02_WIKI/NEGOCIOS/identidad-publica-sirko007.md` §LA CREDENCIAL.
> *(Regenerado el 2026-07-19 para aplicarla: antes ponía solo "10 años".)*

## Regenerar

```bash
python3 _generador_banner_gumroad.py
```
