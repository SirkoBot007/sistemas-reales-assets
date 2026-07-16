# Sistemas Reales — imágenes públicas de la tienda

Imágenes de escaparate (portadas, galerías y miniaturas) de los productos de
[sistemasreales.gumroad.com](https://sistemasreales.gumroad.com).

**Por qué existe este repositorio:** la API de Gumroad exige que las portadas se
enganchen desde una **URL pública** (`POST /v2/products/:id/covers` solo acepta el
parámetro `url`, y rechaza URLs firmadas o privadas). GitHub sirve esas URLs gratis
y de forma estable, sin atar el escaparate del negocio a ninguna suscripción de pago.

**Qué hay aquí:** solo imágenes que ya son públicas en la tienda. Nada privado.

**Norma de las imágenes:** cada captura muestra **contenido real del producto**.
Nada de arte bonito que prometa algo distinto de lo que el comprador recibe.

## Productos

| Carpeta | Producto |
|---|---|
| `prompts-negocio-local/` | Sistema de Prompts de IA para tu Negocio Local (39 págs · 30 prompts) |

Generadas con `_sistema/produccion/crear_galeria_producto.py` (Chrome headless).
