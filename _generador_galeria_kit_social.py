# -*- coding: utf-8 -*-
"""Galerias Kit Freelancer + Social Media Planner — estilo Sistemas Reales, 1280x720,
# NORMA 2026-07-20: NINGUNA imagen lleva el precio del producto dentro.
# El precio lo pone Gumroad y cambia; la imagen no. Ver [[normas-de-alberto]].
Pillow puro. Contenido REAL de los productos (Regla de las imagenes: nada de humo)."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path

W,H=1280,720
BG=(10,14,24); PANEL=(15,21,32); PANEL_B=(34,48,74); CARD=(23,28,40); CARD_B=(42,50,68)
CYAN=(56,189,248); RED=(244,63,94); GREEN=(52,211,153); AMBER=(251,191,36)
VIOLET=(167,139,250)
WHITE=(255,255,255); GRAY=(148,163,184); GRAY2=(100,116,139); MONO_C=(203,213,225)
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
def sello(d,x,y,w,precio):
    rrect(d,[x,y,x+w,y+62],11,fill=(16,34,30),outline=(30,70,60),width=1)
    d.text((x+16,y+12),"SIN IA  ·  SIN CLAVES  ·  SIN CUOTA",font=F(15,bold=True),fill=GREEN)
    d.text((x+16,y+36),precio,font=F(12),fill=GRAY)
def card(d,x,y,w,h,k,v,vcolor=WHITE,ksize=11,vsize=21):
    rrect(d,[x,y,x+w,y+h],11,fill=CARD,outline=CARD_B,width=1)
    d.text((x+16,y+13),k,font=F(ksize,bold=True),fill=GRAY2)
    d.text((x+16,y+34),v,font=F(vsize,bold=True),fill=vcolor)
def footer(d,left,right):
    y=662; d.line([54,y-12,W-54,y-12],fill=(60,70,88),width=1)
    d.text((54,y),left,font=F(12.5),fill=GRAY2)
    d.text((W-54-tw(d,right,F(12.5,bold=True)),y),right,font=F(12.5,bold=True),fill=GRAY)
def pill(d,x,y,txt,col,fillbg):
    w=tw(d,txt,F(12,bold=True))+22
    rrect(d,[x,y,x+w,y+24],12,fill=fillbg,outline=col,width=1)
    d.text((x+11,y+5),txt,font=F(12,bold=True),fill=col); return x+w+8

# ===================== KIT FREELANCER =====================
KDIR=Path(__file__).resolve().parent/"kit-freelancer/galeria"
KDIR.mkdir(parents=True,exist_ok=True)
MK="SISTEMAS REALES  ·  KIT FREELANCER ESENCIAL"
FK="Sistemas Reales · Kit Freelancer Esencial"
def ko(n): return KDIR/n

def k1():
    img=bg_base()
    d,_=header(img,MK,[[("Pon precio, presenta y cobra.",WHITE)],[("Sin improvisar.",CYAN)]],
        "3 herramientas de Excel listas para usar. Rellenas tus datos y funciona.")
    y=258
    items=[("Calculadora de Tarifas","Tu precio/hora mínimo, recomendado y premium",CYAN),
           ("Plantilla de Propuesta","La propuesta que convierte la charla en un «sí»",VIOLET),
           ("Tracker de Clientes","Qué haces, cuánto vale y qué has cobrado",GREEN)]
    for k,v,c in items:
        rrect(d,[54,y,820,y+100],13,fill=PANEL,outline=PANEL_B,width=1)
        dot(d,82,y+50,c,r=8); d.text((104,y+22),k,font=F(20,bold=True),fill=WHITE)
        d.text((104,y+56),v,font=F(15),fill=GRAY); y+=116
    card(d,858,258,368,100,"FORMATOS","Excel · Sheets · LibreOffice",CYAN,vsize=17)
    card(d,858,374,368,100,"GUÍA DE USO","Incluida (PDF paso a paso)",GREEN,vsize=17)
    sello(d,858,490,368,"Kit Freelancer Esencial · pago único")
    footer(d,FK,"1 / 6"); img.save(ko("gal-1-portada.png")); print("k1")

def k2():
    img=bg_base()
    d,_=header(img,MK,[[("«¿Cuánto cobro la hora",WHITE)],[("sin perder dinero?»",CYAN)]],
        "Rellena tus gastos y tus horas. La calculadora te da 3 tarifas al instante.")
    px,py,pw,ph=54,252,640,320
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"TUS DATOS (ejemplo)",font=F(11,bold=True),fill=GRAY2)
    rows=[("Gastos para vivir/trabajar","2.725 € / mes"),
          ("Días × horas al mes","20 × 8"),
          ("% de horas facturables","70 %"),
          ("Margen objetivo","30 %"),
          ("Horas facturables reales","112 h / mes")]
    yy=py+52
    for k,v in rows:
        d.text((px+22,yy),k,font=F(15),fill=GRAY); d.text((px+px+pw-54-tw(d,v,F(16,bold=True)),yy),v,font=F(16,bold=True),fill=WHITE); yy+=48
    card(d,720,268,506,92,"TARIFA MÍNIMA (break-even) · nunca por debajo","24,33 € / h",RED,vsize=26)
    card(d,720,372,506,92,"TARIFA RECOMENDADA (+ margen) · tu precio por defecto","31,63 € / h",GREEN,vsize=26)
    card(d,720,476,506,92,"TARIFA PREMIUM (×2) · urgencias y alto valor","48,66 € / h",AMBER,vsize=26)
    footer(d,FK,"2 / 6"); img.save(ko("gal-2-calculadora.png")); print("k2")

def k3():
    img=bg_base()
    d,_=header(img,MK,[[("La propuesta que",WHITE),(" cierra el trato",VIOLET)]],
        "Rellena los huecos y envíala. Con IVA y totales calculados solos.")
    px,py,pw,ph=54,252,760,320
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"LO QUE INCLUYE LA PLANTILLA",font=F(11,bold=True),fill=GRAY2)
    pts=[("Datos del cliente y referencia de la propuesta",WHITE),
         ("Resumen ejecutivo: problema · solución · resultado",WHITE),
         ("Alcance por 4 fases, con entregable en cada una",WHITE),
         ("«QUÉ NO INCLUYE» → te protege del scope creep",AMBER),
         ("Tabla de inversión con SUBTOTAL + IVA 21 % + TOTAL",GREEN)]
    yy=py+52
    for t,c in pts:
        dot(d,px+24,yy+11,CYAN,r=6); d.text((px+46,yy),t,font=F(16,bold=True if c!=WHITE else False),fill=c); yy+=50
    card(d,838,268,388,140,"IVA Y TOTAL","Automáticos",GREEN,vsize=24)
    # tarjeta CONSEJO con texto ajustado a 2 lineas (evita recorte)
    rrect(d,[838,420,1226,572],11,fill=CARD,outline=CARD_B,width=1)
    d.text((854,433),"CONSEJO",font=F(11,bold=True),fill=GRAY2)
    d.text((854,460),"Expórtala a PDF antes de",font=F(16,bold=True),fill=WHITE)
    d.text((854,484),"enviarla: el cliente no",font=F(16,bold=True),fill=WHITE)
    d.text((854,508),"puede editar tus precios.",font=F(16,bold=True),fill=WHITE)
    footer(d,FK,"3 / 6"); img.save(ko("gal-3-propuesta.png")); print("k3")

def k4():
    img=bg_base()
    d,_=header(img,MK,[[("Todos tus proyectos,",WHITE)],[("en una pantalla.",GREEN)]],
        "Una fila por proyecto. Horas e importes se suman solos abajo.")
    px,py,pw=54,256,1172
    cols=["CLIENTE","PROYECTO","ESTADO","TARIFA/H","H. EST.","TOTAL","FACTURADO"]
    xw=[210,300,150,110,90,120,150]
    rrect(d,[px,py,px+pw,py+236],14,fill=PANEL,outline=PANEL_B,width=1)
    x=px+18; hy=py+16
    for c,w in zip(cols,xw):
        d.text((x,hy),c,font=F(12,bold=True),fill=GRAY2); x+=w
    d.line([px+14,py+42,px+pw-14,py+42],fill=(40,52,74),width=1)
    demo=[("Bar La Plaza","Web + reservas","En curso","35","24","840 €","No",AMBER),
          ("Estudio Nórdico","Branding","Entregado","40","18","720 €","No",AMBER),
          ("Clínica Sonrisa","Campaña ADS","Cobrado","31,63","30","949 €","Sí",GREEN)]
    yy=py+54
    for r in demo:
        x=px+18; vals=r[:7]; stc=r[7]
        for i,(v,w) in enumerate(zip(vals,xw)):
            col=stc if i in (2,6) else WHITE if i in(0,) else GRAY
            d.text((x,yy),v,font=F(14,bold=(i in(0,2,6))),fill=col); x+=w
        yy+=42
    d.line([px+14,yy+4,px+pw-14,yy+4],fill=(40,52,74),width=1)
    d.text((px+18,yy+14),"TOTALES",font=F(13,bold=True),fill=CYAN)
    d.text((px+18+210+300+150+110,yy+14),"72 h",font=F(14,bold=True),fill=WHITE)
    d.text((px+18+210+300+150+110+90,yy+14),"2.509 €",font=F(14,bold=True),fill=GREEN)
    footer(d,FK,"4 / 6"); img.save(ko("gal-4-tracker.png")); print("k4")

def k5():
    img=bg_base()
    d,_=header(img,MK,[[("No te dejamos solo",WHITE)],[("ante la hoja en blanco.",CYAN)]],
        "Guía de uso en PDF incluida: cada herramienta explicada paso a paso.")
    y=250
    steps=[("Cómo abrir","Excel, Google Sheets o LibreOffice. Sin instalar nada.",CYAN),
           ("Qué rellenar","Las celdas con ejemplos [así] se sustituyen por lo tuyo.",VIOLET),
           ("Cómo leerlo","Qué significa cada tarifa y cada total, en cristiano.",GREEN),
           ("El flujo completo","Calcula → propone → registra. El ciclo con cada cliente.",AMBER)]
    for k,v,c in steps:
        rrect(d,[54,y,1226,y+82],13,fill=PANEL,outline=PANEL_B,width=1)
        rrect(d,[78,y+24,84,y+58],3,fill=c)
        d.text((104,y+16),k,font=F(19,bold=True),fill=WHITE)
        d.text((104,y+46),v,font=F(15),fill=GRAY); y+=98
    footer(d,FK,"5 / 6"); img.save(ko("gal-5-guia.png")); print("k5")

def k6():
    img=bg_base()
    d,_=header(img,MK,[[("Herramientas de verdad.",WHITE)],[("Tuyas para siempre.",GREEN)]],
        "Pago único. Sin cuotas, sin registro, sin depender de ninguna app.")
    yes=[("Se abre en Excel, Sheets y LibreOffice (gratis)"),
         ("Fórmulas ya puestas: tú solo escribes en las celdas"),
         ("Guía de uso en PDF paso a paso, incluida"),
         ("Editable al 100 %: cambia IVA, márgenes y % a tu país")]
    no=[("No es un curso ni una suscripción"),
        ("No necesita internet ni cuenta"),
        ("No pide claves de IA ni programar")]
    rrect(d,[54,256,644,584],14,fill=(14,30,26),outline=(30,70,60),width=1)
    d.text((78,276),"LO QUE SÍ",font=F(13,bold=True),fill=GREEN); yy=316
    for t in yes:
        dot(d,80,yy+9,GREEN,r=6); d.text((100,yy),t,font=F(15),fill=WHITE); yy+=52
    rrect(d,[668,256,1226,584],14,fill=(30,18,22),outline=(70,34,40),width=1)
    d.text((692,276),"LO QUE NO",font=F(13,bold=True),fill=RED); yy=316
    for t in no:
        d.text((694,yy-2),"×",font=F(20,bold=True),fill=RED); d.text((716,yy),t,font=F(15),fill=GRAY); yy+=52
    sello(d,692,470,510,"Kit Freelancer Esencial · pago único")
    footer(d,FK,"6 / 6"); img.save(ko("gal-6-que-si-que-no.png")); print("k6")

# ===================== SOCIAL PLANNER =====================
SDIR=Path(__file__).resolve().parent/"social-planner-2026/galeria"
SDIR.mkdir(parents=True,exist_ok=True)
MS="SISTEMAS REALES  ·  SOCIAL MEDIA CONTENT PLANNER 2026"
FS="Sistemas Reales · Social Media Content Planner 2026"
def so(n): return SDIR/n

def s1():
    img=bg_base()
    d,_=header(img,MS,[[("Un año de contenido,",WHITE)],[("planificado en un Excel.",CYAN)]],
        "Qué publicar, cuándo y con qué objetivo. Sin improvisar cada semana.")
    y=256
    items=[("Dashboard anual","Se rellena solo desde las hojas de los meses",CYAN),
           ("12 hojas de meses","Calendario ya montado: Ene → Dic",VIOLET),
           ("Banco de hashtags","Grupos por nicho, listos para pegar",GREEN),
           ("Fórmulas virales","10 patrones de titular que funcionan",AMBER)]
    x=54
    for k,v,c in items:
        rrect(d,[x,y,x+286,y+150],13,fill=PANEL,outline=PANEL_B,width=1)
        dot(d,x+22,y+34,c,r=7); d.text((x+40,y+24),k,font=F(15,bold=True),fill=WHITE)
        d.text((x+22,y+64),v,font=F(13),fill=GRAY); x+=294
    sello(d,54,440,560,"Social Media Content Planner 2026 · pago único")
    card(d,634,440,592,62,"15 HOJAS · 1 SOLO ARCHIVO","Excel · Google Sheets · LibreOffice",CYAN,vsize=16)
    footer(d,FS,"1 / 6"); img.save(so("gal-1-portada.png")); print("s1")

def s2():
    img=bg_base()
    d,_=header(img,MS,[[("El Dashboard ",WHITE),("se rellena solo.",CYAN)]],
        "Rellenas los meses y él cuenta posts, publicados y reach automáticamente.")
    px,py,pw=54,250,1172
    rrect(d,[px,py,px+pw,py+150],14,fill=PANEL,outline=PANEL_B,width=1)
    cols=["MES","POSTS PLAN.","POSTS PUB.","REACH EST.","OBJETIVO DEL MES"]
    xw=[150,180,180,190,470]
    x=px+20
    for c,w in zip(cols,xw): d.text((x,py+16),c,font=F(12,bold=True),fill=GRAY2); x+=w
    d.line([px+16,py+40,px+pw-16,py+40],fill=(40,52,74),width=1)
    rows=[("Enero","13","9","24.500","Arranque de año · nuevos seguidores"),
          ("Febrero","12","12","31.200","San Valentín · campaña de gratitud"),
          ("Noviembre","13","8","58.900","Black Friday · conversión máxima")]
    yy=py+52
    for r in rows:
        x=px+20
        for i,(v,w) in enumerate(zip(r,xw)):
            col=CYAN if i==3 else WHITE if i==0 else GRAY
            d.text((x,yy),v,font=F(14,bold=(i in(0,3))),fill=col); x+=w
        yy+=32
    # pilares
    py2=430
    rrect(d,[px,py2,px+pw,py2+142],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+20,py2+16),"LOS 4 PILARES DE CONTENIDO (reparto recomendado)",font=F(12,bold=True),fill=GRAY2)
    pil=[("EDUCA","40 %",GREEN),("ENTRETIENE","25 %",CYAN),("VENDE","20 %",AMBER),("CONECTA","15 %",VIOLET)]
    x=px+20; cw=283
    for name,pct,c in pil:
        rrect(d,[x,py2+50,x+cw-14,py2+126],11,fill=CARD,outline=CARD_B,width=1)
        d.text((x+16,py2+62),name,font=F(14,bold=True),fill=c)
        d.text((x+16,py2+86),pct,font=F(30,bold=True),fill=WHITE); x+=cw
    footer(d,FS,"2 / 6"); img.save(so("gal-2-dashboard.png")); print("s2")

def s3():
    img=bg_base()
    d,_=header(img,MS,[[("Cada mes, ",WHITE),("ya montado.",VIOLET)]],
        "Días, plataformas y pilares repartidos. Tú solo pones el tema y publicas.")
    px,py,pw=54,250,1172
    rrect(d,[px,py,px+pw,py+322],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+20,py+16),"HOJA «ENE» — ENERO 2026  ·  objetivo: arranque de año",font=F(12,bold=True),fill=AMBER)
    cols=["DÍA","PLATAFORMA","PILAR","FORMATO","TEMA / TÍTULO","ESTADO"]
    xw=[110,190,150,150,380,190]
    x=px+20
    for c,w in zip(cols,xw): d.text((x,py+50),c,font=F(12,bold=True),fill=GRAY2); x+=w
    d.line([px+16,py+74,px+pw-16,py+74],fill=(40,52,74),width=1)
    rows=[("2 Vie","Instagram","EDUCA","Carrusel","5 errores de precio que cometes","Publicado",GREEN),
          ("5 Lun","TikTok","ENTRETIENE","Reel","Un día en mi negocio (detrás)","Publicado",GREEN),
          ("7 Mié","LinkedIn","VENDE","Post","Cómo te ayudo en 3 pasos","Planificado",GRAY2),
          ("9 Vie","Newsletter","CONECTA","Email","Pregunta de la semana","Planificado",GRAY2),
          ("12 Lun","YouTube","EDUCA","Vídeo","Tutorial: tu primera landing","Planificado",GRAY2)]
    yy=py+86
    for r in rows:
        x=px+20
        for i,(v,w) in enumerate(zip(r[:6],xw)):
            col=r[6] if i==5 else (CYAN if i==2 else (WHITE if i in(0,4) else GRAY))
            d.text((x,yy),v,font=F(13,bold=(i in(2,5))),fill=col); x+=w
        yy+=44
    footer(d,FS,"3 / 6"); img.save(so("gal-3-mes.png")); print("s3")

def s4():
    img=bg_base()
    d,_=header(img,MS,[[("La regla de oro:",WHITE)],[("no seas solo un vendedor.",AMBER)]],
        "El reparto 40/25/20/15 que hace crecer una cuenta sin quemar a la gente.")
    pil=[("EDUCA","40 %","Aporta valor y te posiciona como experto","Carruseles, tutoriales, hilos",GREEN),
         ("ENTRETIENE","25 %","Genera shares y conexión emocional","Reels, memes de nicho, storytelling",CYAN),
         ("VENDE","20 %","Lleva a tu producto o servicio","Stories con enlace, posts con CTA",AMBER),
         ("CONECTA","15 %","Humaniza la marca y crea comunidad","Encuestas, Q&A, día a día",VIOLET)]
    y=248
    for name,pct,obj,fmt,c in pil:
        rrect(d,[54,y,1226,y+84],13,fill=PANEL,outline=PANEL_B,width=1)
        rrect(d,[78,y+18,190,y+66],10,fill=CARD,outline=c,width=1)
        d.text((94,y+22),name,font=F(13,bold=True),fill=c)
        d.text((94,y+42),pct,font=F(23,bold=True),fill=WHITE)
        d.text((214,y+18),obj,font=F(16,bold=True),fill=WHITE)
        d.text((214,y+46),"Formatos ideales: "+fmt,font=F(14),fill=GRAY); y+=98
    footer(d,FS,"4 / 6"); img.save(so("gal-4-pilares.png")); print("s4")

def s5():
    img=bg_base()
    d,_=header(img,MS,[[("Hashtags y titulares,",WHITE)],[("resueltos.",CYAN)]],
        "Nunca más te quedas en blanco: copia, rota y aplica una fórmula probada.")
    px,py=54,252
    rrect(d,[px,py,px+574,py+320],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+20,py+16),"BANCO DE HASHTAGS · por nicho",font=F(12,bold=True),fill=GRAY2)
    nichos=["Marketing digital","Emprendimiento","Finanzas","Fitness y salud","Moda y lifestyle"]
    yy=py+52
    for n in nichos:
        dot(d,px+22,yy+9,CYAN,r=6); d.text((px+42,yy),n,font=F(16,bold=True),fill=WHITE); yy+=42
    d.text((px+20,yy+6),"Copia el grupo de tu nicho y RÓTALO cada 3-4 posts.",font=F(13),fill=GRAY)
    px2=652
    rrect(d,[px2,py,px2+574,py+320],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px2+20,py+16),"FÓRMULAS VIRALES · 10 patrones de titular",font=F(12,bold=True),fill=GRAY2)
    forms=[("Hook numérico","5 errores que [audiencia] comete con…"),
           ("Hook secreto","Lo que nadie te dice sobre…"),
           ("Transformación","De 0 a mis primeros 5.000 € en 90 días"),
           ("Controversia","Opinión impopular: el contenido diario NO…"),
           ("Storytelling 3 actos","Situación › conflicto › resolución")]
    yy=py+50
    for k,v in forms:
        d.text((px2+20,yy),"› "+k,font=F(14,bold=True),fill=AMBER)
        d.text((px2+34,yy+20),v,font=F(13,mono=False),fill=GRAY); yy+=54
    footer(d,FS,"5 / 6"); img.save(so("gal-5-hashtags-formulas.png")); print("s5")

def s6():
    img=bg_base()
    d,_=header(img,MS,[[("Un plan claro vale más",WHITE)],[("que mil ideas sueltas.",GREEN)]],
        "Guía de uso incluida (hoja dentro del Excel + PDF). Pago único, sin cuotas.")
    y=250
    flow=[("Domingo, 15 min","Escribe el tema de los posts de la semana",CYAN),
          ("Apóyate en una fórmula","Elige un titular probado y rellénalo",VIOLET),
          ("Al publicar","Marca «Publicado» y pega tus hashtags",GREEN),
          ("Fin de mes","Apunta reach real y repite lo que funcionó",AMBER)]
    for k,v,c in flow:
        rrect(d,[54,y,760,y+82],13,fill=PANEL,outline=PANEL_B,width=1)
        rrect(d,[78,y+24,84,y+58],3,fill=c)
        d.text((104,y+16),k,font=F(18,bold=True),fill=WHITE)
        d.text((104,y+46),v,font=F(14),fill=GRAY); y+=98
    card(d,792,256,434,120,"GUÍA DE USO","Hoja en el Excel + PDF aparte",GREEN,vsize=18)
    card(d,792,392,434,120,"FUNCIONA EN","Excel · Sheets · LibreOffice",CYAN,vsize=18)
    sello(d,792,528,434,"Pago único, sin cuotas")
    footer(d,FS,"6 / 6"); img.save(so("gal-6-cierre.png")); print("s6")

if __name__=="__main__":
    for fn in (k1,k2,k3,k4,k5,k6,s1,s2,s3,s4,s5,s6): fn()
    print("OK galerias generadas")
