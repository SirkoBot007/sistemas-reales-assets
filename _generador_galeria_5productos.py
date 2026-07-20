# -*- coding: utf-8 -*-
"""Galerias Sistemas Reales — 5 productos, 6 imgs 1280x720, Pillow puro, contenido REAL."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
BASE="/sessions/quirky-brave-knuth/mnt/CEREBRO-DIGITAL-ALBERTO/_recursos/_assets-publicos"
W,H=1280,720
BG=(10,14,24); PANEL=(15,21,32); PANEL_B=(34,48,74); CARD=(23,28,40); CARD_B=(42,50,68)
CYAN=(56,189,248); RED=(244,63,94); GREEN=(52,211,153); AMBER=(251,191,36); VIOLET=(167,139,250)
WHITE=(255,255,255); GRAY=(148,163,184); GRAY2=(100,116,139)
FD="/usr/share/fonts/truetype/dejavu"
def F(sz,bold=False,mono=False):
    f=("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf") if mono else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(f"{FD}/{f}",int(sz))
def bg_base():
    img=Image.new("RGB",(W,H),BG); glow=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(glow)
    gd.ellipse([820,-260,1500,320],fill=(20,40,60)); gd.ellipse([-260,460,360,1000],fill=(30,26,48))
    return Image.blend(img,glow.filter(ImageFilter.GaussianBlur(150)),0.85)
def rrect(d,xy,r,fill=None,outline=None,width=1): d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)
def tw(d,s,f): return d.textlength(s,font=f)
def dot(d,x,cy,color,r=7): d.ellipse([x,cy-r,x+2*r,cy+r],fill=color)
def header(img,marca,title_segs,sub):
    d=ImageDraw.Draw(img); x=54
    d.text((x,42),marca,font=F(13,bold=True),fill=CYAN); y=66
    for seg in title_segs:
        cx=x
        for t,c in seg:
            d.text((cx,y),t,font=F(38,bold=True),fill=c); cx+=tw(d,t,F(38,bold=True))
        y+=48
    d.text((x,y+4),sub,font=F(17),fill=GRAY); return d,y+40
def card(d,x,y,w,h,k,v,vcolor=WHITE,ksize=11,vsize=21):
    rrect(d,[x,y,x+w,y+h],11,fill=CARD,outline=CARD_B,width=1)
    d.text((x+16,y+13),k,font=F(ksize,bold=True),fill=GRAY2)
    d.text((x+16,y+34),v,font=F(vsize,bold=True),fill=vcolor)
def sello(d,x,y,w,linea1,linea2,col=GREEN,bg=(16,34,30),ob=(30,70,60)):
    rrect(d,[x,y,x+w,y+62],11,fill=bg,outline=ob,width=1)
    d.text((x+16,y+12),linea1,font=F(15,bold=True),fill=col)
    d.text((x+16,y+36),linea2,font=F(12),fill=GRAY)
def footer(d,left,right):
    y=662; d.line([54,y-12,W-54,y-12],fill=(60,70,88),width=1)
    d.text((54,y),left,font=F(12.5),fill=GRAY2)
    d.text((W-54-tw(d,right,F(12.5,bold=True)),y),right,font=F(12.5,bold=True),fill=GRAY)
def bullets(d,x,y,items,w=760,lh=50,fs=16):
    for t,c in items:
        dot(d,x,y+11,CYAN,r=6); d.text((x+22,y),t,font=F(fs,bold=(c!=GRAY)),fill=c); y+=lh
    return y
def panel(d,x,y,w,h,title):
    rrect(d,[x,y,x+w,y+h],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((x+22,y+16),title,font=F(11,bold=True),fill=GRAY2)

def outdir(slug):
    p=Path(f"{BASE}/{slug}/galeria"); p.mkdir(parents=True,exist_ok=True); return p
def save(img,slug,name): img.save(outdir(slug)/name); print(slug,name)

# ============ 1) FACTURAS PACK COMPLETO (PRO) 25 € — facturas-n8n-pro ============
S="facturas-n8n-pro"; MK="SISTEMAS REALES · FACTURAS AUTOMÁTICO · PACK COMPLETO"; FT="Sistemas Reales · Facturas Automático (Pack Completo)"
def f_pro():
    img=bg_base(); d,_=header(img,MK,[[("Lee tus facturas con IA",WHITE)],[("en TU ordenador.",CYAN)]],
        "Saca proveedor, fecha, concepto e importe y te avisa al móvil. Sin nube, sin cuota, sin claves.")
    card(d,54,258,286,96,"VELOCIDAD","~12,5 s / factura",CYAN,vsize=22)
    card(d,352,258,286,96,"COSTE","0 € · IA local",GREEN,vsize=22)
    card(d,650,258,286,96,"MODELO","qwen2.5-coder:7b",VIOLET,vsize=19)
    card(d,948,258,278,96,"AVISO","Telegram",AMBER,vsize=22)
    panel(d,54,372,1172,196,"LO QUE LLEVAS")
    bullets(d,80,410,[("Workflow n8n PRO con umbral de confianza configurable",WHITE),
        ("5 prompts por tipo de factura + 6 facturas de prueba realistas",WHITE),
        ("Guía de instalación en 10 pasos + doc de 7 errores comunes",WHITE)],lh=44)
    sello(d,880,404,346,"SIN NUBE · SIN CLAVES · SIN CUOTA","Pack Completo · 25 € · pago único")
    footer(d,FT,"1 / 6"); save(img,S,"gal-1-portada.png")
def f_pro2():
    img=bg_base(); d,_=header(img,MK,[[("De un PDF a 4 datos limpios,",WHITE)],[("en segundos.",CYAN)]],
        "La IA extrae los campos en JSON. Si no lee bien una factura, NO se la inventa.")
    panel(d,54,258,600,300,"LA IA DEVUELVE (ejemplo)")
    rows=[("proveedor","Suministros García S.L."),("fecha","14/03/2026"),("concepto","Material de oficina"),
          ("total","148,50 €"),("confianza","0,94")]
    yy=300
    for k,v in rows:
        d.text((80,yy),k,font=F(15,mono=True),fill=GRAY); d.text((320,yy),v,font=F(16,bold=True),fill=WHITE); yy+=46
    card(d,690,258,536,140,"FLUJO","PDF → IA local → clasifica → Telegram",CYAN,vsize=18)
    rrect(d,[690,414,1226,558],11,fill=(40,30,16),outline=(90,70,30),width=1)
    d.text((708,430),"EL CASO AMARILLO",font=F(11,bold=True),fill=AMBER)
    d.text((708,458),"Factura borrosa o rara → baja la",font=F(16,bold=True),fill=WHITE)
    d.text((708,482),"confianza y la marca REVISAR.",font=F(16,bold=True),fill=WHITE)
    d.text((708,512),"Mejor 10 s tuyos que un error de 300 €.",font=F(14),fill=GRAY)
    footer(d,FT,"2 / 6"); save(img,S,"gal-2-que-hace.png")
def f_pro3():
    img=bg_base(); d,_=header(img,MK,[[("Tú decides cuándo",WHITE),(" revisar.",AMBER)]],
        "Lo que hace PRO al pack: el umbral de confianza es configurable (viene en 0,7).")
    panel(d,54,258,1172,150,"NODO ‘Configuración (umbral)’  →  umbral_confianza = 0,7")
    card(d,80,300,540,88,"CONFIANZA ≥ UMBRAL","La factura pasa como OK",GREEN,vsize=20)
    card(d,660,300,540,88,"CONFIANZA < UMBRAL","Se marca REVISAR (amarillo)",AMBER,vsize=20)
    panel(d,54,426,1172,132,"AJÚSTALO A TU GUSTO")
    bullets(d,80,462,[("¿Salen demasiadas a revisar? Baja el umbral a 0,6",GRAY),
        ("¿Quieres más control? Súbelo. El nodo ‘Clasificar’ lo lee solo",GRAY)],lh=40,fs=15)
    footer(d,FT,"3 / 6"); save(img,S,"gal-3-umbral.png")
def f_pro4():
    img=bg_base(); d,_=header(img,MK,[[("6 facturas de prueba,",WHITE)],[("una por cada caso real.",CYAN)]],
        "Para que pruebes cada tipo antes de usarlo con las tuyas.")
    items=[("Tipo A","Proveedor único (limpia)",GREEN),("Tipo B","Multilínea (varias líneas)",CYAN),
           ("Tipo C","Escaneada / torcida",VIOLET),("Tipo D","Recibo tipo Stripe",AMBER),
           ("Tipo E","IVA desglosado (10% y 21%)",GREEN),("Tipo F","Campo ilegible → REVISAR",RED)]
    x0,y0=54,258;w,h=380,140;gx,gy=16,16
    for i,(k,v,c) in enumerate(items):
        x=x0+(i%3)*(w+gx); y=y0+(i//3)*(h+gy)
        rrect(d,[x,y,x+w,y+h],12,fill=CARD,outline=CARD_B,width=1)
        dot(d,x+22,y+34,c,r=8); d.text((x+42,y+22),k,font=F(19,bold=True),fill=WHITE)
        d.text((x+22,y+70),v,font=F(15),fill=GRAY)
    footer(d,FT,"4 / 6"); save(img,S,"gal-4-facturas-prueba.png")
def f_pro5():
    img=bg_base(); d,_=header(img,MK,[[("5 prompts afinados",WHITE),(" por tipo.",VIOLET)]],
        "Cambia el prompt del nodo de IA según la factura y afina la extracción.")
    items=[("prompt-base","El general, sirve para casi todo",CYAN),
           ("prompt-factura-proveedor-unico","Facturas simples de un proveedor",GREEN),
           ("prompt-factura-multilinea","Varias líneas → devuelve la suma total",VIOLET),
           ("prompt-plataformas-digitales","Stripe / PayPal / Amazon Business",AMBER),
           ("prompt-ticket-escaneado","Baja calidad · nunca inventa cifras",RED)]
    y=258
    for k,v,c in items:
        rrect(d,[54,y,1226,y+76],11,fill=CARD,outline=CARD_B,width=1)
        dot(d,80,y+38,c,r=7); d.text((104,y+16),k+".txt",font=F(17,bold=True,mono=True),fill=WHITE)
        d.text((104,y+44),v,font=F(15),fill=GRAY); y+=86
    footer(d,FT,"5 / 6"); save(img,S,"gal-5-prompts.png")
def f_pro6():
    img=bg_base(); d,_=header(img,MK,[[("Tus facturas ",WHITE),("no salen de tu equipo.",GREEN)]],
        "Todo corre en local. Cero dependencia de la nube y cero cuotas mensuales.")
    items=[("SIN IA en la nube","La IA corre en tu ordenador (Ollama)",GREEN),
           ("SIN claves ni API","No pagas por token ni por servicio externo",GREEN),
           ("SIN cuota mensual","Pago único. Es tuyo para siempre",GREEN),
           ("7 errores resueltos","Doc con causa y solución de cada fallo",CYAN)]
    x0,y0=54,262;w,h=580,132;gx,gy=12,16
    for i,(k,v,c) in enumerate(items):
        x=x0+(i%2)*(w+gx); y=y0+(i//2)*(h+gy)
        rrect(d,[x,y,x+w,y+h],12,fill=CARD,outline=CARD_B,width=1)
        d.text((x+22,y+24),k,font=F(20,bold=True),fill=c); d.text((x+22,y+64),v,font=F(15),fill=GRAY)
    footer(d,FT,"@sistemasreales · Pack Completo 25 €"); save(img,S,"gal-6-garantias.png")

# ============ 2) FACTURAS PLANTILLA n8n (GRATIS) — facturas-n8n-free ============
S2="facturas-n8n-free"; MK2="SISTEMAS REALES · FACTURAS AUTOMÁTICO · PLANTILLA GRATIS"; FT2="Sistemas Reales · Facturas Automático (Plantilla n8n)"
def g1():
    img=bg_base(); d,_=header(img,MK2,[[("El sistema del vídeo,",WHITE)],[("gratis y montado en 10 pasos.",GREEN)]],
        "Lee facturas con IA local y te avisa por Telegram. Sin nube, sin suscripciones.")
    card(d,54,258,286,96,"PRECIO","GRATIS",GREEN,vsize=24)
    card(d,352,258,286,96,"VELOCIDAD","~12,5 s / factura",CYAN,vsize=20)
    card(d,650,258,286,96,"COSTE USO","0 € · IA local",GREEN,vsize=20)
    card(d,948,258,278,96,"AVISO","Telegram",AMBER,vsize=22)
    panel(d,54,372,1172,196,"LO QUE LLEVAS")
    bullets(d,80,410,[("Workflow n8n listo para importar (1 archivo)",WHITE),
        ("2 facturas de prueba (una limpia + una borrosa para el caso amarillo)",WHITE),
        ("README con la instalación completa en 10 pasos",WHITE)],lh=44)
    sello(d,880,404,346,"SIN NUBE · SIN CLAVES · SIN CUOTA","Plantilla n8n · GRATIS")
    footer(d,FT2,"1 / 6"); save(img,S2,"gal-1-portada.png")
def g2():
    img=bg_base(); d,_=header(img,MK2,[[("Proveedor, fecha, concepto",WHITE)],[("e importe. Automático.",CYAN)]],
        "Y si una factura está borrosa, la marca para revisar en vez de inventarse el número.")
    panel(d,54,258,600,300,"LA IA DEVUELVE (ejemplo)")
    rows=[("proveedor","Bar La Esquina"),("fecha","03/02/2026"),("concepto","Consumición"),("total","42,00 €"),("confianza","0,88")]
    yy=300
    for k,v in rows:
        d.text((80,yy),k,font=F(15,mono=True),fill=GRAY); d.text((320,yy),v,font=F(16,bold=True),fill=WHITE); yy+=46
    rrect(d,[690,258,1226,558],11,fill=(40,30,16),outline=(90,70,30),width=1)
    d.text((712,278),"EL INDICADOR AMARILLO",font=F(12,bold=True),fill=AMBER)
    d.text((712,318),"Foto borrosa o formato raro →",font=F(17,bold=True),fill=WHITE)
    d.text((712,344),"baja la confianza y marca REVISAR.",font=F(17,bold=True),fill=WHITE)
    d.text((712,392),"Eso es correcto: la IA no inventa.",font=F(15),fill=GRAY)
    d.text((712,418),"Mejor 10 s tuyos que un error",font=F(15),fill=GRAY)
    d.text((712,442),"de 300 € en tu contabilidad.",font=F(15),fill=GRAY)
    footer(d,FT2,"2 / 6"); save(img,S2,"gal-2-que-hace.png")
def g3():
    img=bg_base(); d,_=header(img,MK2,[[("De cero a funcionando",WHITE)],[("en 10 pasos.",CYAN)]],
        "Sin saber programar. Cada paso está explicado en el README.")
    steps=["Instala Docker Desktop y arráncalo","Arranca n8n en localhost:5678","Instala Ollama + modelo qwen2.5-coder:7b",
           "Importa el workflow en n8n","Crea tu bot con @BotFather","Pon tu credencial y chatId de Telegram",
           "Execute Workflow: procesa los ejemplos","Prueba con tus PDFs reales"]
    x0,y0=54,256;w,h=580,72;gx,gy=12,12
    for i,s in enumerate(steps):
        x=x0+(i%2)*(w+gx); y=y0+(i//2)*(h+gy)
        rrect(d,[x,y,x+w,y+h],10,fill=CARD,outline=CARD_B,width=1)
        d.ellipse([x+16,y+22,x+44,y+50],fill=(20,40,60))
        n=str(i+1); d.text((x+30-tw(d,n,F(15,bold=True))/2,y+27),n,font=F(15,bold=True),fill=CYAN)
        d.text((x+58,y+26),s,font=F(14.5,bold=True),fill=WHITE)
    footer(d,FT2,"3 / 6"); save(img,S2,"gal-3-10-pasos.png")
def g4():
    img=bg_base(); d,_=header(img,MK2,[[("2 facturas de prueba",WHITE)],[("para entender el sistema.",CYAN)]],
        "Una limpia (sale OK) y una borrosa (activa el caso amarillo).")
    card(d,54,266,580,150,"FACTURA OK","Limpia y realista → pasa como OK",GREEN,vsize=19)
    card(d,646,266,580,150,"FACTURA BORROSA","Verosímil → se marca REVISAR",AMBER,vsize=19)
    panel(d,54,438,1172,120,"REQUISITOS")
    d.text((80,478),"Un ordenador normal (probado: Ryzen 7 4800H, 16 GB RAM, SIN gráfica pro).  ~12,5 s/factura.  0 €.",font=F(15),fill=GRAY)
    footer(d,FT2,"4 / 6"); save(img,S2,"gal-4-pruebas.png")
def g5():
    img=bg_base(); d,_=header(img,MK2,[[("Todo en tu equipo.",WHITE)],[("Cero cuotas.",GREEN)]],
        "La IA corre en tu ordenador. Tus facturas no salen de casa.")
    items=[("SIN IA en la nube","La IA corre en local (Ollama)",GREEN),
           ("SIN claves ni API","No pagas por token ni servicio",GREEN),
           ("SIN cuota","Gratis, y es tuyo para siempre",GREEN),
           ("Privado","Tus PDFs nunca se suben a nadie",CYAN)]
    x0,y0=54,262;w,h=580,132;gx,gy=12,16
    for i,(k,v,c) in enumerate(items):
        x=x0+(i%2)*(w+gx); y=y0+(i//2)*(h+gy)
        rrect(d,[x,y,x+w,y+h],12,fill=CARD,outline=CARD_B,width=1)
        d.text((x+22,y+24),k,font=F(20,bold=True),fill=c); d.text((x+22,y+64),v,font=F(15),fill=GRAY)
    footer(d,FT2,"5 / 6"); save(img,S2,"gal-5-garantias.png")
def g6():
    img=bg_base(); d,_=header(img,MK2,[[("¿Quieres el sistema",WHITE)],[("completo?",AMBER)]],
        "Esta plantilla es el episodio gratis. El Pack Completo lleva más.")
    panel(d,54,258,1172,220,"EL PACK COMPLETO (25 €) AÑADE")
    bullets(d,80,300,[("6 facturas de prueba en vez de 2 (proveedor, multilínea, Stripe, IVA…)",WHITE),
        ("5 prompts afinados por tipo de factura",WHITE),
        ("Umbral de confianza configurable (decides cuándo revisar)",WHITE),
        ("Guía de instalación paso a paso + 7 errores comunes",WHITE)],lh=42)
    footer(d,FT2,"@sistemasreales · Suscríbete: es gratis"); save(img,S2,"gal-6-pack-completo.png")

# ============ 3) PACK EMAIL MARKETING 17 € — emails-marketing ============
S3="emails-marketing"; MK3="SISTEMAS REALES · PACK EMAIL MARKETING PROFESIONAL"; FT3="Sistemas Reales · Pack Plantillas Email Marketing"
def e1():
    img=bg_base(); d,_=header(img,MK3,[[("5 emails profesionales,",WHITE)],[("listos para copiar y pegar.",CYAN)]],
        "Plantillas HTML que pegas en tu ESP y personalizas en minutos. Sin diseñar nada.")
    card(d,54,258,286,96,"PLANTILLAS","5 emails HTML",CYAN,vsize=20)
    card(d,352,258,286,96,"FORMATO","HTML listo",GREEN,vsize=20)
    card(d,650,258,286,96,"USO","Copia y pega",VIOLET,vsize=20)
    card(d,948,258,278,96,"GUÍA","Incluida (Excel)",AMBER,vsize=18)
    panel(d,54,372,1172,196,"PARA QUÉ SIRVEN")
    bullets(d,80,410,[("Cubren el ciclo completo: captar, vender, recuperar y fidelizar",WHITE),
        ("Compatibles con Mailchimp, ActiveCampaign, Klaviyo, Brevo, MailerLite",WHITE),
        ("Solo reemplazas las [VARIABLES] con tus datos y envías",WHITE)],lh=44)
    sello(d,880,404,346,"HTML LISTO · MÓVIL Y ESCRITORIO","Pack 5 plantillas · 17 €",col=CYAN,bg=(14,28,40),ob=(30,60,90))
    footer(d,FT3,"1 / 6"); save(img,S3,"gal-1-portada.png")
def e2():
    img=bg_base(); d,_=header(img,MK3,[[("Las 5 plantillas",WHITE),(" del pack.",CYAN)]],
        "Una para cada momento clave de tu relación con el suscriptor.")
    items=[("01 · Bienvenida","Nuevo suscriptor · entrega el lead magnet",CYAN),
           ("02 · Lanzamiento de producto","Día de lanzamiento · máxima conversión",VIOLET),
           ("03 · Abandono de carrito","1h después · recupera la venta con bono",AMBER),
           ("04 · Reactivación","Inactivos +60 días · reenganchar o limpiar",GREEN),
           ("05 · Newsletter semanal","Fidelidad + autoridad + venta suave",CYAN)]
    y=258
    for k,v,c in items:
        rrect(d,[54,y,1226,y+76],11,fill=CARD,outline=CARD_B,width=1)
        dot(d,80,y+38,c,r=7); d.text((104,y+16),k,font=F(18,bold=True),fill=WHITE)
        d.text((104,y+44),v,font=F(15),fill=GRAY); y+=86
    footer(d,FT3,"2 / 6"); save(img,S3,"gal-2-plantillas.png")
def e3():
    img=bg_base(); d,_=header(img,MK3,[[("De archivo a campaña",WHITE)],[("en 3 pasos.",GREEN)]],
        "No necesitas saber HTML. Se pega y se rellena.")
    steps=[("1","Abre el HTML y copia todo (Ctrl+A, Ctrl+C)"),("2","Pega en tu ESP: Crear campaña → Editor HTML"),
           ("3","Reemplaza las [VARIABLES] con tus datos"),("4","Envíate una prueba (móvil + escritorio) y lanza")]
    y=262
    for n,s in steps:
        rrect(d,[54,y,1226,y+80],11,fill=CARD,outline=CARD_B,width=1)
        d.ellipse([78,y+24,110,y+56],fill=(16,34,30)); d.text((88,y+29),n,font=F(17,bold=True),fill=GREEN)
        d.text((130,y+28),s,font=F(17,bold=True),fill=WHITE); y+=92
    footer(d,FT3,"3 / 6"); save(img,S3,"gal-3-como-usar.png")
def e4():
    img=bg_base(); d,_=header(img,MK3,[[("Funciona en tu ",WHITE),("ESP favorito.",VIOLET)]],
        "Pegas el HTML y listo. Compatible con las herramientas más usadas.")
    esps=["Mailchimp","ActiveCampaign","Klaviyo","Brevo","MailerLite","y cualquier editor HTML"]
    x0,y0=54,262;w,h=380,110;gx,gy=16,16
    cols=[CYAN,GREEN,VIOLET,AMBER,RED,GRAY]
    for i,name in enumerate(esps):
        x=x0+(i%3)*(w+gx); y=y0+(i//3)*(h+gy)
        rrect(d,[x,y,x+w,y+h],12,fill=CARD,outline=CARD_B,width=1)
        dot(d,x+24,y+55,cols[i],r=8); d.text((x+46,y+42),name,font=F(19,bold=True),fill=WHITE)
    footer(d,FT3,"4 / 6"); save(img,S3,"gal-4-compatibles.png")
def e5():
    img=bg_base(); d,_=header(img,MK3,[[("Cada plantilla ya trae",WHITE)],[("lo que convierte.",CYAN)]],
        "Estructura pensada para vender, no un HTML vacío.")
    panel(d,54,258,1172,300,"DENTRO DE CADA EMAIL")
    bullets(d,80,300,[("Cabecera y preheader listos para tu marca",WHITE),
        ("Cuerpo con jerarquía clara: gancho → beneficio → prueba",WHITE),
        ("Botón de llamada a la acción (CTA) destacado",AMBER),
        ("Bloques de [VARIABLES] señalados para que no te pierdas",GREEN),
        ("Diseño que se ve bien en móvil y escritorio",WHITE)],lh=46)
    footer(d,FT3,"5 / 6"); save(img,S3,"gal-5-anatomia.png")
def e6():
    img=bg_base(); d,_=header(img,MK3,[[("Copia, personaliza",WHITE),(" y envía.",GREEN)]],
        "Ahorra horas de diseño y redacción con plantillas ya probadas.")
    items=[("5 plantillas HTML","Ciclo completo de email marketing",CYAN),
           ("Guía de uso incluida","Excel con qué es cada email y cuándo enviarlo",GREEN),
           ("Personalizable","Cambia colores, textos y CTA en minutos",VIOLET),
           ("Pago único","17 € · sin cuotas, tuyo para siempre",AMBER)]
    x0,y0=54,262;w,h=580,132;gx,gy=12,16
    for i,(k,v,c) in enumerate(items):
        x=x0+(i%2)*(w+gx); y=y0+(i//2)*(h+gy)
        rrect(d,[x,y,x+w,y+h],12,fill=CARD,outline=CARD_B,width=1)
        d.text((x+22,y+24),k,font=F(19,bold=True),fill=c); d.text((x+22,y+64),v,font=F(14.5),fill=GRAY)
    footer(d,FT3,"@sistemasreales · Pack Email 17 €"); save(img,S3,"gal-6-cierre.png")

# ============ 4) TRACKER FINANZAS 2026 15 € — tracker-finanzas-2026 ============
S4="tracker-finanzas-2026"; MK4="SISTEMAS REALES · TRACKER DE FINANZAS PERSONALES 2026"; FT4="Sistemas Reales · Tracker de Finanzas Personales 2026"
def t1():
    img=bg_base(); d,_=header(img,MK4,[[("Controla tu dinero",WHITE)],[("todo el año 2026.",CYAN)]],
        "Ingresos, gastos, ahorro y tasa de ahorro. Rellenas números y el dashboard se hace solo.")
    card(d,54,258,286,96,"HOJAS","14 (Dashboard+12 meses+guía)",CYAN,vsize=14)
    card(d,352,258,286,96,"CATEGORÍAS","8 bloques preparados",GREEN,vsize=17)
    card(d,650,258,286,96,"DASHBOARD","Se actualiza solo",VIOLET,vsize=18)
    card(d,948,258,278,96,"FORMATO","Excel · Sheets · LO",AMBER,vsize=16)
    panel(d,54,372,1172,196,"PARA QUÉ SIRVE")
    bullets(d,80,410,[("Ves de un vistazo cuánto entra, cuánto sale y cuánto ahorras cada mes",WHITE),
        ("La tasa de ahorro te dice si vas bien (10% ok · 20%+ excelente)",WHITE),
        ("Sin saber de Excel: solo escribes números en la hoja del mes",WHITE)],lh=44)
    sello(d,880,404,346,"SIN CUOTA · SIN APPS · ES TUYO","Tracker 2026 · 15 € · pago único")
    footer(d,FT4,"1 / 6"); save(img,S4,"gal-1-portada.png")
def t2():
    img=bg_base(); d,_=header(img,MK4,[[("El dashboard anual,",WHITE)],[("automático.",GREEN)]],
        "Rellenas los meses y esta tabla se calcula sola. Ejemplo con Enero relleno:")
    panel(d,54,256,1172,240,"RESUMEN ANUAL 2026")
    cols=["MES","INGRESOS","GASTOS","AHORRO","TASA"]; xs=[80,340,560,780,1000]
    for x,c in zip(xs,cols): d.text((x,290),c,font=F(13,bold=True),fill=GRAY2)
    data=[("Enero","2.500 €","950 €","1.550 €","62%",GREEN),("Febrero","—","—","—","—",GRAY2),
          ("…","","","","",GRAY2),("TOTAL","2.500 €","950 €","1.550 €","62%",CYAN)]
    y=326
    for row in data:
        c=row[-1]
        for x,val in zip(xs,row[:-1]): d.text((x,y),val,font=F(16,bold=(c!=GRAY2)),fill=(WHITE if c!=GRAY2 else GRAY2) if x!=xs[-1] else c)
        y+=40
    d.text((80,506),"AHORRO = ingresos − gastos.   TASA = % de tus ingresos que ahorras.",font=F(15),fill=GRAY)
    footer(d,FT4,"2 / 6"); save(img,S4,"gal-2-dashboard.png")
def t3():
    img=bg_base(); d,_=header(img,MK4,[[("Tus categorías",WHITE),(" ya preparadas.",CYAN)]],
        "Cada mes trae presupuesto, real y diferencia. Solo rellenas.")
    cats=["Vivienda","Alimentación","Transporte","Ocio & Personal","Salud","Finanzas","Familia","Gastos varios"]
    x0,y0=54,262;w,h=282,84;gx,gy=14,14
    cols=[CYAN,GREEN,VIOLET,AMBER,RED,CYAN,GREEN,VIOLET]
    for i,cat in enumerate(cats):
        x=x0+(i%4)*(w+gx); y=y0+(i//4)*(h+gy)
        rrect(d,[x,y,x+w,y+h],11,fill=CARD,outline=CARD_B,width=1)
        dot(d,x+20,y+42,cols[i],r=7); d.text((x+40,y+30),cat,font=F(16,bold=True),fill=WHITE)
    panel(d,54,438,1172,120,"CÓMO FUNCIONA")
    d.text((80,478),"Escribe lo que planeas gastar (PRESUPUESTO) y lo que gastas de verdad (REAL). La DIFERENCIA se calcula sola.",font=F(15),fill=GRAY)
    footer(d,FT4,"3 / 6"); save(img,S4,"gal-3-categorias.png")
def t4():
    img=bg_base(); d,_=header(img,MK4,[[("Tu número clave:",WHITE)],[("la tasa de ahorro.",GREEN)]],
        "El % de tus ingresos que consigues guardar cada mes. Súbelo poco a poco.")
    card(d,54,270,380,150,"10%","Un buen comienzo",AMBER,vsize=44)
    card(d,452,270,380,150,"20%+","Excelente",GREEN,vsize=44)
    card(d,850,270,376,150,"AUTO","Se calcula sola",CYAN,vsize=34)
    panel(d,54,446,1172,112,"EL HÁBITO QUE LO CAMBIA TODO")
    d.text((80,486),"Dedica 10 minutos el último día de cada mes a actualizar el tracker. Ese hábito mejora tus finanzas de verdad.",font=F(15),fill=GRAY)
    footer(d,FT4,"4 / 6"); save(img,S4,"gal-4-tasa.png")
def t5():
    img=bg_base(); d,_=header(img,MK4,[[("14 hojas,",WHITE),(" todo el año cubierto.",CYAN)]],
        "Un dashboard, una guía y una hoja por cada mes de 2026.")
    tags=["DASHBOARD","Guía de uso","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    x=70;y=290;lh=64
    for i,t in enumerate(tags):
        wt=tw(d,t,F(15,bold=True))+34
        if x+wt>1210: x=70; y+=lh
        col= CYAN if i==0 else (GREEN if i==1 else VIOLET)
        rrect(d,[x,y,x+wt,y+44],12,fill=CARD,outline=col,width=1)
        d.text((x+17,y+12),t,font=F(15,bold=True),fill=WHITE); x+=wt+12
    panel(d,54,470,1172,88,"")
    d.text((80,500),"Abre en Excel, Google Sheets o LibreOffice. Guía de uso incluida dentro del archivo.",font=F(16,bold=True),fill=WHITE)
    footer(d,FT4,"5 / 6"); save(img,S4,"gal-5-hojas.png")
def t6():
    img=bg_base(); d,_=header(img,MK4,[[("Empieza en menos",WHITE)],[("de 10 minutos.",GREEN)]],
        "Herramienta lista para usar, no una plantilla vacía que hay que montar.")
    items=[("Se actualiza solo","El dashboard suma tus 12 meses automático",GREEN),
           ("Guía incluida","Paso a paso dentro del propio archivo",CYAN),
           ("Compatible","Excel · Google Sheets · LibreOffice",VIOLET),
           ("Pago único","15 € · sin cuotas ni apps que instalar",AMBER)]
    x0,y0=54,262;w,h=580,132;gx,gy=12,16
    for i,(k,v,c) in enumerate(items):
        x=x0+(i%2)*(w+gx); y=y0+(i//2)*(h+gy)
        rrect(d,[x,y,x+w,y+h],12,fill=CARD,outline=CARD_B,width=1)
        d.text((x+22,y+24),k,font=F(19,bold=True),fill=c); d.text((x+22,y+64),v,font=F(14.5),fill=GRAY)
    footer(d,FT4,"@sistemasreales · Tracker 2026 · 15 €"); save(img,S4,"gal-6-cierre.png")

# ============ 5) PACK 200+ PROMPTS 19 € — prompts-200-negocios ============
S5="prompts-200-negocios"; MK5="SISTEMAS REALES · PACK 200+ PROMPTS IA PARA NEGOCIOS"; FT5="Sistemas Reales · Pack 200+ Prompts IA para Negocios"
def p1():
    img=bg_base(); d,_=header(img,MK5,[[("204 prompts profesionales",WHITE)],[("para tu negocio.",CYAN)]],
        "Copia y pega en ChatGPT, Claude o Gemini. Cada uno con rol, contexto y formato de salida.")
    card(d,54,258,286,96,"PROMPTS","204 listos",CYAN,vsize=22)
    card(d,352,258,286,96,"CATEGORÍAS","8 áreas",GREEN,vsize=22)
    card(d,650,258,286,96,"COMPATIBLE","ChatGPT·Claude·Gemini",VIOLET,vsize=14)
    card(d,948,258,278,96,"USO","Copia y pega",AMBER,vsize=20)
    panel(d,54,372,1172,196,"CÓMO ESTÁN HECHOS")
    bullets(d,80,410,[("Cada prompt lleva rol + contexto + formato de salida pedido",WHITE),
        ("Solo reemplazas las [VARIABLES EN MAYÚSCULAS] con tus datos",WHITE),
        ("Organizados en 8 pestañas con autofiltro para buscar por palabra",WHITE)],lh=44)
    sello(d,880,404,346,"204 PROMPTS · 8 CATEGORÍAS","Pack Prompts · 19 € · pago único",col=VIOLET,bg=(26,20,42),ob=(60,45,95))
    footer(d,FT5,"1 / 6"); save(img,S5,"gal-1-portada.png")
def p2():
    img=bg_base(); d,_=header(img,MK5,[[("8 categorías,",WHITE),(" 204 prompts.",CYAN)]],
        "Cubren todo lo que necesita un negocio para funcionar con IA.")
    items=[("Marketing Digital","26",CYAN),("Copywriting & Ventas","26",VIOLET),
           ("Redes Sociales & Contenido","26",AMBER),("Productividad & Gestión","25",GREEN),
           ("Finanzas & Negocios","25",CYAN),("Emprendimiento & Estrategia","25",VIOLET),
           ("Educación & Formación","25",AMBER),("IA para Empresas & Automatización","26",GREEN)]
    x0,y0=54,258;w,h=580,84;gx,gy=12,12
    for i,(k,n,c) in enumerate(items):
        x=x0+(i%2)*(w+gx); y=y0+(i//2)*(h+gy)
        rrect(d,[x,y,x+w,y+h],11,fill=CARD,outline=CARD_B,width=1)
        dot(d,x+20,y+42,c,r=7); d.text((x+40,y+30),k,font=F(16,bold=True),fill=WHITE)
        d.text((x+w-64,y+28),n,font=F(22,bold=True),fill=c)
    d.text((54,646-2),"",font=F(12),fill=GRAY)
    footer(d,FT5,"2 / 6 · TOTAL 204 prompts"); save(img,S5,"gal-2-categorias.png")
def p3():
    img=bg_base(); d,_=header(img,MK5,[[("Anatomía de un ",WHITE),("prompt.",VIOLET)]],
        "Ejemplo real: ‘Estrategia de marketing a 90 días’ (prompt nº 1).")
    panel(d,54,256,1172,302,"PROMPT COMPLETO (extracto)")
    lines=["Actúa como director de marketing con 15 años de experiencia lanzando","negocios digitales. Mi negocio es [NEGOCIO] y vende [PRODUCTO/SERVICIO]",
           "a [CLIENTE IDEAL]. Mi presupuesto mensual es [PRESUPUESTO] € y mi objetivo","en 90 días es [OBJETIVO MEDIBLE]. Diseña una estrategia trimestral en 3 fases…"]
    y=296
    for ln in lines:
        d.text((80,y),ln,font=F(15.5,mono=True),fill=(203,213,225)); y+=34
    y+=8
    d.text((80,y),"→ Rol",font=F(14,bold=True),fill=CYAN); d.text((200,y),"→ Contexto con [VARIABLES]",font=F(14,bold=True),fill=AMBER)
    d.text((560,y),"→ Formato de salida pedido",font=F(14,bold=True),fill=GREEN)
    footer(d,FT5,"3 / 6"); save(img,S5,"gal-3-anatomia.png")
def p4():
    img=bg_base(); d,_=header(img,MK5,[[("Sácale el máximo",WHITE)],[("en 4 pasos.",GREEN)]],
        "De copiar el prompt a tener un resultado de nivel profesional.")
    steps=[("1","Copia el prompt completo y pégalo en tu IA"),("2","Reemplaza las [VARIABLES] con tus datos reales"),
           ("3","¿No te convence? Pide: ‘hazlo más concreto’, ‘dame 3 alternativas’"),("4","Encadena prompts: usa una respuesta como base de la siguiente")]
    y=262
    for n,s in steps:
        rrect(d,[54,y,1226,y+80],11,fill=CARD,outline=CARD_B,width=1)
        d.ellipse([78,y+24,110,y+56],fill=(26,20,42)); d.text((88,y+29),n,font=F(17,bold=True),fill=VIOLET)
        d.text((130,y+28),s,font=F(16,bold=True),fill=WHITE); y+=92
    footer(d,FT5,"4 / 6"); save(img,S5,"gal-4-como-usar.png")
def p5():
    img=bg_base(); d,_=header(img,MK5,[[("Funcionan en ",WHITE),("cualquier IA.",CYAN)]],
        "Los mismos prompts sirven en las tres grandes. Elige según la tarea.")
    esps=[("ChatGPT","GPT-4 / GPT-5",GREEN),("Claude","Opus / Sonnet",VIOLET),("Gemini","Pro / Flash",CYAN)]
    x0,y0=54,268;w,h=380,150;gx=16
    for i,(k,v,c) in enumerate(esps):
        x=x0+i*(w+gx)
        rrect(d,[x,y0,x+w,y0+h],12,fill=CARD,outline=CARD_B,width=1)
        d.text((x+24,y0+34),k,font=F(26,bold=True),fill=c); d.text((x+24,y0+82),v,font=F(16),fill=GRAY)
    panel(d,54,444,1172,114,"CONSEJO")
    d.text((80,484),"Los modelos más potentes (Claude Opus, GPT-4/5, Gemini Pro) rinden mejor en tareas complejas o largas.",font=F(15),fill=GRAY)
    footer(d,FT5,"5 / 6"); save(img,S5,"gal-5-compatibles.png")
def p6():
    img=bg_base(); d,_=header(img,MK5,[[("Deja de escribir prompts",WHITE)],[("desde cero.",GREEN)]],
        "204 prompts probados, organizados y listos para tu día a día.")
    items=[("204 prompts","8 categorías de negocio",VIOLET),
           ("Autofiltro","Busca por palabra clave en cada pestaña",CYAN),
           ("Todo en un Excel","Una pestaña por área, fácil de navegar",GREEN),
           ("Pago único","19 € · sin cuotas, tuyo para siempre",AMBER)]
    x0,y0=262-0,262;w,h=580,132;gx,gy=12,16; x0=54
    for i,(k,v,c) in enumerate(items):
        x=x0+(i%2)*(w+gx); y=y0+(i//2)*(h+gy)
        rrect(d,[x,y,x+w,y+h],12,fill=CARD,outline=CARD_B,width=1)
        d.text((x+22,y+24),k,font=F(19,bold=True),fill=c); d.text((x+22,y+64),v,font=F(14.5),fill=GRAY)
    footer(d,FT5,"@sistemasreales · Pack Prompts 19 €"); save(img,S5,"gal-6-cierre.png")

for fn in [f_pro,f_pro2,f_pro3,f_pro4,f_pro5,f_pro6, g1,g2,g3,g4,g5,g6, e1,e2,e3,e4,e5,e6, t1,t2,t3,t4,t5,t6, p1,p2,p3,p4,p5,p6]:
    fn()
print("TODAS OK")
