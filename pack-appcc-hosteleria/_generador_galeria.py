# -*- coding: utf-8 -*-
"""Galeria Pack APPCC — estilo Sistemas Reales, 1280x720, Pillow puro."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
W,H=1280,720
OUT=Path(__file__).resolve().parent / "galeria"; OUT.mkdir(parents=True,exist_ok=True)
BG=(10,14,24);PANEL=(15,21,32);PANEL_B=(34,48,74);CARD=(23,28,40);CARD_B=(42,50,68)
CYAN=(56,189,248);RED=(244,63,94);GREEN=(52,211,153);AMBER=(251,191,36)
WHITE=(255,255,255);GRAY=(148,163,184);GRAY2=(100,116,139);MONO_C=(203,213,225);BLUE=(96,165,250)
CMAP={'red':RED,'green':GREEN,'amber':AMBER,'cyan':CYAN,'blue':BLUE}
FD="/usr/share/fonts/truetype/dejavu"
def F(sz,bold=False,mono=False):
    sz=int(sz)
    f=("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf") if mono else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(f"{FD}/{f}",sz)
def bg_base():
    img=Image.new("RGB",(W,H),BG);glow=Image.new("RGB",(W,H),BG);gd=ImageDraw.Draw(glow)
    gd.ellipse([820,-260,1500,320],fill=(20,40,60));gd.ellipse([-260,460,360,1000],fill=(40,20,30))
    return Image.blend(img,glow.filter(ImageFilter.GaussianBlur(150)),0.85)
def rrect(d,xy,r,fill=None,outline=None,width=1):d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)
def tw(d,s,font):return d.textlength(s,font=font)
def dot(d,x,cy,color,r=7):d.ellipse([x,cy-r,x+2*r,cy+r],fill=color)
def warn(d,x,cy,color=AMBER):
    d.polygon([(x+9,cy-8),(x+18,cy+8),(x,cy+8)],fill=color);d.text((x+6,cy-6),"!",font=F(12,bold=True),fill=(20,20,20))
def marker(d,mk,x,cy):
    if mk in CMAP:dot(d,x,cy,CMAP[mk])
    elif mk=='warn':warn(d,x,cy)
def header(img,marca,title_lines,sub):
    d=ImageDraw.Draw(img);x=54;d.text((x,42),marca,font=F(13,bold=True),fill=CYAN);y=66
    for seg in title_lines:
        cx=x
        for t,c in seg:
            d.text((cx,y),t,font=F(38,bold=True),fill=c);cx+=tw(d,t,F(38,bold=True))
        y+=48
    d.text((x,y+4),sub,font=F(17),fill=GRAY);return d,y+40
def block(d,px,py,pad,lines):
    yy=py
    for mk,s,f,c,dy in lines:
        if mk:
            asc=f.getmetrics()[0];marker(d,mk,px+pad,yy+asc*0.55);d.text((px+pad+24,yy),s,font=f,fill=c)
        elif s:d.text((px+pad,yy),s,font=f,fill=c)
        yy+=dy
    return yy
def sello(d,x,y,w):
    rrect(d,[x,y,x+w,y+62],11,fill=(16,34,30),outline=(30,70,60),width=1)
    d.text((x+16,y+12),"SIN IA  ·  SIN CLAVES  ·  SIN CUOTA",font=F(15,bold=True),fill=GREEN)
    d.text((x+16,y+36),"Un termómetro no necesita inteligencia artificial",font=F(12),fill=GRAY)
def card(d,x,y,w,h,k,v,vsmall="",vcolor=WHITE):
    rrect(d,[x,y,x+w,y+h],11,fill=CARD,outline=CARD_B,width=1)
    d.text((x+16,y+13),k,font=F(11,bold=True),fill=GRAY2);d.text((x+16,y+32),v,font=F(21,bold=True),fill=vcolor)
    if vsmall:d.text((x+16+tw(d,v,F(21,bold=True))+8,y+41),vsmall,font=F(12),fill=GRAY)
def footer(d,left,right):
    y=662;d.line([54,y-12,W-54,y-12],fill=(60,70,88),width=1)
    d.text((54,y),left,font=F(12.5),fill=GRAY2);d.text((W-54-tw(d,right,F(12.5,bold=True)),y),right,font=F(12.5,bold=True),fill=GRAY)
def save(img,name):p=OUT/name;img.save(p);print("OK",name,p.stat().st_size//1024,"KB")

def img1():
    img=bg_base()
    d,_=header(img,"SISTEMAS REALES  ·  n8n PARA HOSTELERÍA",
        [[("Los dos registros del ",WHITE),("APPCC",CYAN),(" que",WHITE)],
         [("peor se llevan. Resueltos.",WHITE)]],
        "Temperaturas y limpieza, por Telegram. El papel de la puerta de la cámara, bien hecho.")
    px,py,pw,ph=54,268,700,360
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"LO QUE TE PUEDE COSTAR DINERO",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+50,22,[
        ('red',"Registros incompletos = infracción leve",F(15,bold=True),WHITE,28),
        (None,"hasta 3.000 € — por el papel, aunque tus cámaras",F(14),GRAY,24),
        (None,"estén perfectas. Reglamento (CE) 852/2004.",F(14),GRAY,34),
        ('amber',"La hoja rellenada de golpe el día que avisan",F(15,bold=True),AMBER,26),
        (None,"El mismo boli, la misma letra. Un inspector lo ve",F(13),GRAY,22),
        (None,"de lejos. Aquí cada línea lleva su hora de verdad.",F(13),GRAY,34),
        ('green',"Se contesta por el móvil, en 5 segundos",F(15,bold=True),GREEN,24),
        (None,"con las manos mojadas y a media comanda.",F(13),GRAY,24),
    ])
    cx,cw=786,440
    card(d,cx,268,cw,74,"DOS SISTEMAS","Temp. + Limpieza","misma hoja, mismo bot")
    card(d,cx,352,cw,74,"MULTA LEVE QUE EVITA","hasta 3.000 €","por registro incompleto",vcolor=RED)
    card(d,cx,436,cw,74,"SE INSTALA TOCANDO","1 nodo","el nodo ⚙️ CONFIG")
    sello(d,cx,520,cw)
    footer(d,"Los dos comparten hoja y bot: es un sistema, no dos cosas sueltas","Alberto Landa · 25 años en hostelería · 10 al frente de un mesón")
    save(img,"01-portada-pack.png")

def img2():
    img=bg_base()
    d,_=header(img,"SISTEMA 1  ·  REGISTRO DE TEMPERATURAS",
        [[("Dos avisos al día. ",WHITE),("Contestas y",CYAN)],
         [("queda registrado con hora real.",WHITE)]],
        "A las 9:00 y a las 20:00 te llega el aviso. El cocinero contesta una línea.")
    px,py,pw,ph=54,268,720,360
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"EL GRUPO DE TELEGRAM DE LA COCINA",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+48,22,[
        (None,"09:00  🔔 Toca medir: cámara 1, congelador, caliente",F(13.5,mono=True),GRAY,30),
        (None,"Cocinero:  camara1 3.5",F(14.5,mono=True),WHITE,26),
        ('green',"Apuntado · Cámara refrigeración 1 · dentro de límite",F(13.5),GREEN,30),
        (None,"Cocinero:  congela -19,5",F(14.5,mono=True),WHITE,26),
        ('green',"Apuntado · acepta coma decimal · da igual mayúsculas",F(13.5),GREEN,34),
        (None,"Cada línea: fecha, hora y QUIÉN lo apuntó.",F(14,bold=True),WHITE,24),
        (None,"Nadie tiene que acordarse de nada.",F(13.5),GRAY,24),
    ])
    cx,cw=798,428
    card(d,cx,268,cw,74,"LECTURAS EXIGIDAS","mínimo 2/día","por punto de control")
    card(d,cx,352,cw,74,"PUNTOS DE CONTROL","los que tengas","cámaras, congela, caliente…")
    card(d,cx,436,cw,74,"LÍMITES","los pones TÚ","de tu plan, no de una plantilla")
    sello(d,cx,520,cw)
    footer(d,"Se rellena solo en una hoja de Google llamada 'Temperaturas'","Esa hoja ES tu registro")
    save(img,"02-temperaturas-aviso.png")

def img3():
    img=bg_base()
    d,_=header(img,"SISTEMA 1  ·  LO QUE NO HACE NINGÚN OTRO",
        [[("Una desviación ",WHITE),("sin medida correctora",RED)],
         [("es PEOR que no tener registro.",WHITE)]],
        "Cuando algo se sale del límite, el bot NO lo apunta y se calla. Te pregunta.")
    px,py,pw,ph=54,258,720,378
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"CUANDO LA TEMPERATURA SE SALE",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+48,22,[
        (None,"Cocinero:  caliente 61",F(14.5,mono=True),WHITE,32),
        ('red',"Mantenimiento en caliente: 61 °C",F(15,bold=True),RED,26),
        (None,"Fuera de límite (65 a 99 °C).",F(13.5,mono=True),GRAY,30),
        (None,"NO lo apunto todavía. Dime qué has hecho:",F(14,bold=True),WHITE,24),
        (None,"caliente 61 he subido el baño maría",F(14,mono=True),CYAN,34),
        ('amber',"Apuntado CON la acción escrita",F(15,bold=True),AMBER,26),
        (None,"No hay forma de meter una desviación",F(13.5),GRAY,22),
        (None,"huérfana en tu registro.",F(13.5),GRAY,22),
    ])
    cx,cw=798,428
    rrect(d,[cx,258,cx+cw,258+180],12,fill=CARD,outline=CARD_B,width=1)
    block(d,cx-22,278,44,[
        (None,"El inspector no busca",F(15,bold=True),WHITE,26),
        (None,"temperaturas perfectas.",F(15,bold=True),WHITE,30),
        (None,"Sospecha de ellas.",F(14),GRAY,28),
        (None,"Busca qué HICISTE",F(14.5,bold=True),CYAN,24),
        (None,"cuando se torció.",F(14.5,bold=True),CYAN,24),
    ])
    card(d,cx,458,cw,74,"REGISTRO HUÉRFANO","imposible","el bot lo bloquea",vcolor=GREEN)
    sello(d,cx,548,cw)
    footer(d,"Un APPCC bien llevado TIENE desviaciones — lo que no puede tener es desviaciones sin explicar","Sistemas Reales")
    save(img,"03-temperaturas-desviacion.png")

def img4():
    img=bg_base()
    d,_=header(img,"SISTEMA 1  ·  EL INFORME",
        [[("Un informe ",WHITE),("escrito para el inspector",CYAN)],
         [("el día 1 de cada mes.",WHITE)]],
        "Llega solo. O lo pides con /appcc. Solo te aprueba si no hay huérfanas ni días en blanco.")
    px,py,pw,ph=54,268,760,368
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"📋 Mesón Viña T — registro APPCC (30 días)",font=F(13,bold=True),fill=WHITE)
    block(d,px,py+48,22,[
        (None,"4 lecturas en 2 días",F(13.5,mono=True),GRAY,32),
        (None,"Lo que te puede costar dinero:",F(14,bold=True),AMBER,30),
        ('red',"1 desviación sin medida correctora",F(14.5,bold=True),WHITE,24),
        (None,"Es lo PRIMERO que mira un inspector.",F(13),GRAY,22),
        (None,"· 2026-07-16 09:10 — caliente: 61 °C",F(13,mono=True),MONO_C,30),
        ('amber',"28 días sin ningún registro",F(14.5,bold=True),WHITE,26),
        ('amber',"7 lecturas que faltan (mínimo 2/día)",F(14.5,bold=True),WHITE,30),
        (None,"Registros incompletos = infracción leve = hasta 3.000 €",F(13,bold=True),RED,24),
    ])
    cx,cw=838,388
    card(d,cx,268,cw,80,"APROBADO RASPADO","no existe","o te defiende o no",vcolor=CYAN)
    card(d,cx,360,cw,80,"RELLENAR HACIA ATRÁS","imposible","cada línea lleva su hora",vcolor=GREEN)
    card(d,cx,452,cw,80,"LO PIDES CUANDO QUIERAS","/appcc","informe al instante")
    sello(d,cx,544,cw)
    footer(d,"No hay aprobado raspado: o el registro te defiende, o no","El informe dice la verdad")
    save(img,"04-temperaturas-informe.png")

def img5():
    img=bg_base()
    d,_=header(img,"SISTEMA 2  ·  REGISTRO DE LIMPIEZA",
        [[("Cada zona con ",WHITE),("su frecuencia",CYAN),(",",WHITE)],
         [("y te avisa cuando te pasas.",WHITE)]],
        "La cocina es diaria, la campana mensual, los desagües semanales. Se mide contra TU plan.")
    px,py,pw,ph=54,268,760,368
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"EL REPASO DE LAS 11:00 — SOLO SI HAY ALGO",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+50,22,[
        ('red',"Campana extractora y filtros   mensual",F(14,mono=True,bold=True),WHITE,24),
        (None,"hace 136 días  ←  106 días de retraso",F(13.5,mono=True),RED,34),
        ('amber',"Almacén y estanterías   semanal",F(14,mono=True,bold=True),WHITE,24),
        (None,"hace 26 días  ←  19 días de retraso",F(13.5,mono=True),AMBER,34),
        ('green',"Suelos y superficies de cocina   diaria",F(14,mono=True,bold=True),WHITE,24),
        (None,"hace 0 días  ·  al día",F(13.5,mono=True),GREEN,34),
        (None,"Un checklist pregunta '¿limpiaste hoy?'.",F(13.5),GRAY,22),
        (None,"Eso no vale: cada zona tiene SU frecuencia.",F(13.5,bold=True),WHITE,22),
    ])
    cx,cw=838,388
    card(d,cx,268,cw,80,"FRECUENCIAS QUE ENTIENDE","8","diaria → anual")
    card(d,cx,360,cw,80,"EL AVISO","11:00","y solo si hay algo fuera")
    card(d,cx,452,cw,80,"FRECUENCIAS","las de TU plan","no las de una plantilla")
    sello(d,cx,544,cw)
    footer(d,"Un aviso que dice 'todo bien' cada día se silencia en una semana","Este solo aparece cuando hay algo")
    save(img,"05-limpieza-frecuencias.png")

def img6():
    img=bg_base()
    d,_=header(img,"SISTEMA 2  ·  Y CAZA LO QUE NO SE HIZO NUNCA",
        [[("Tu registro puede ser la ",WHITE),("prueba",GREEN)],
         [("de que cumples… o de que ",WHITE),("no",RED),(".",WHITE)]],
        "Es el mismo papel: depende de cómo lo lleves. Por eso este avisa ANTES, no después.")
    px,py,pw,ph=54,268,720,368
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"ZONAS QUE JAMÁS APARECEN EN EL REGISTRO",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+50,22,[
        ('amber',"2 zonas sin registrar NUNCA",F(15,bold=True),AMBER,28),
        (None,"· Barra y tiradores  (diaria)",F(13.5,mono=True),MONO_C,24),
        (None,"· Revisión control de plagas  (trimestral)",F(13.5,mono=True),MONO_C,34),
        (None,"Están en tu plan APPCC. Si están en el plan",F(13.5),GRAY,22),
        (None,"y no en el registro, es PEOR que si no",F(13.5),GRAY,22),
        (None,"estuvieran.",F(13.5),GRAY,32),
        (None,"limpieza extractora  →  lo reconoce por el",F(13,mono=True),CYAN,22),
        (None,"nombre, no hace falta el id exacto.",F(13,mono=True),CYAN,22),
    ])
    cx,cw=798,428
    rrect(d,[cx,268,cx+cw,268+150],12,fill=CARD,outline=CARD_B,width=1)
    block(d,cx-22,286,44,[
        (None,"El primer mes va a salir",F(14.5,bold=True),WHITE,26),
        (None,"todo rojo. No limpiáis peor:",F(14),GRAY,26),
        (None,"antes no se medía. Aguanta",F(14),GRAY,26),
        (None,"y se pone verde solo.",F(14.5,bold=True),GREEN,24),
    ])
    card(d,cx,438,cw,74,"VALE DECIRLO DE 5 FORMAS","limpieza · limpio · hecho","lo demás lo ignora")
    sello(d,cx,528,cw)
    footer(d,"Podéis usar el mismo grupo para hablar: lo que no reconoce, lo ignora","Consejo de quien ha estado detrás")
    save(img,"06-limpieza-nunca.png")

def img7():
    img=bg_base()
    d,_=header(img,"POR QUÉ SIN IA — Y ES A PROPÓSITO",
        [[("Cero claves. Cero facturas",WHITE)],
         [("sorpresa. Cero ",WHITE),("números inventados",CYAN),(".",WHITE)]],
        "Una IA, ante un dato raro, se lo inventa. Un número inventado en un registro APPCC es peor que un hueco.")
    px,py,pw,ph=54,268,720,368
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"LO QUE PASA SI FALLA — TE LO CUENTO ANTES",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+50,22,[
        ('green',"Si se cae Telegram: no ves confirmación",F(14),WHITE,22),
        (None,"= no está apuntado. Se escribe otra vez.",F(13),GRAY,30),
        ('green',"Si falla Sheets: n8n lo marca en rojo",F(14),WHITE,22),
        (None,"botón Retry y el dato entra.",F(13),GRAY,30),
        ('green',"Si escriben mal: pregunta, no adivina",F(14),WHITE,22),
        (None,"y no guarda nada hasta entenderlo.",F(13),GRAY,30),
        ('green',"Si el equipo deja de apuntar: el informe",F(14),WHITE,22),
        (None,"dirá la verdad — 'X días en blanco'.",F(13),GRAY,22),
    ])
    cx,cw=798,428
    card(d,cx,268,cw,74,"WORKFLOWS","2","temperaturas + limpieza")
    card(d,cx,352,cw,74,"SE TOCA","1 nodo","el ⚙️ CONFIG, sin código")
    card(d,cx,436,cw,74,"SOPORTE","su correo","contesta él, no un ticket")
    sello(d,cx,520,cw)
    footer(d,"25 años en hostelería · 10 al frente de un mesón en Madrid · 4,7★ · +300 reseñas","He pasado esas inspecciones")
    save(img,"07-pack-sin-ia.png")

for f in (img1,img2,img3,img4,img5,img6,img7): f()
print("== TOTAL ==", len(list(OUT.glob('*.png'))))
