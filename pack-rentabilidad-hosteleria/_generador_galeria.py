# -*- coding: utf-8 -*-
"""Galeria Pack RENTABILIDAD — estilo Sistemas Reales, 1280x720, Pillow puro.
Sin emojis de fuente (DejaVu no los tiene): los marcadores se DIBUJAN."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1280, 720
OUT = Path(__file__).resolve().parent / "galeria"
OUT.mkdir(parents=True, exist_ok=True)

BG=(10,14,24); PANEL=(15,21,32); PANEL_B=(34,48,74); CARD=(23,28,40); CARD_B=(42,50,68)
CYAN=(56,189,248); RED=(244,63,94); GREEN=(52,211,153); AMBER=(251,191,36)
WHITE=(255,255,255); GRAY=(148,163,184); GRAY2=(100,116,139); MONO_C=(203,213,225)
BLACKDOT=(90,100,120)
CMAP={'red':RED,'green':GREEN,'amber':AMBER,'cyan':CYAN,'black':BLACKDOT}

FD="/usr/share/fonts/truetype/dejavu"
def F(sz,bold=False,mono=False):
    sz=int(sz)
    f=("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf") if mono else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(f"{FD}/{f}",sz)

def bg_base():
    img=Image.new("RGB",(W,H),BG); glow=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(glow)
    gd.ellipse([820,-260,1500,320],fill=(20,40,60)); gd.ellipse([-260,460,360,1000],fill=(40,20,30))
    return Image.blend(img,glow.filter(ImageFilter.GaussianBlur(150)),0.85)

def rrect(d,xy,r,fill=None,outline=None,width=1): d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)
def tw(d,s,font): return d.textlength(s,font=font)

def dot(d,x,cy,color,r=7):
    d.ellipse([x,cy-r,x+2*r,cy+r],fill=color)
def warn(d,x,cy,color=AMBER):
    d.polygon([(x+9,cy-8),(x+18,cy+8),(x,cy+8)],fill=color)
    d.text((x+6,cy-6),"!",font=F(12,bold=True),fill=(20,20,20))

def marker(d,mk,x,cy):
    if mk in CMAP: dot(d,x,cy,CMAP[mk])
    elif mk=='warn': warn(d,x,cy)

def header(img,marca,title_lines,sub):
    d=ImageDraw.Draw(img); x=54
    d.text((x,42),marca,font=F(13,bold=True),fill=CYAN); y=66
    for seg in title_lines:
        cx=x
        for t,c in seg:
            d.text((cx,y),t,font=F(38,bold=True),fill=c); cx+=tw(d,t,F(38,bold=True))
        y+=48
    d.text((x,y+4),sub,font=F(17),fill=GRAY); return d,y+40

def block(d,px,py,pad,lines):
    """lines: (marker|None, text, font, color, dy)"""
    yy=py
    for mk,s,f,c,dy in lines:
        if mk:
            asc=f.getmetrics()[0]; marker(d,mk,px+pad,yy+asc*0.55)
            d.text((px+pad+24,yy),s,font=f,fill=c)
        elif s:
            d.text((px+pad,yy),s,font=f,fill=c)
        yy+=dy
    return yy

def sello(d,x,y,w):
    rrect(d,[x,y,x+w,y+62],11,fill=(16,34,30),outline=(30,70,60),width=1)
    d.text((x+16,y+12),"SIN IA  ·  SIN CLAVES  ·  SIN CUOTA",font=F(15,bold=True),fill=GREEN)
    d.text((x+16,y+36),"Nunca te llega una factura sorpresa",font=F(12),fill=GRAY)

def card(d,x,y,w,h,k,v,vsmall="",vcolor=WHITE):
    rrect(d,[x,y,x+w,y+h],11,fill=CARD,outline=CARD_B,width=1)
    d.text((x+16,y+13),k,font=F(11,bold=True),fill=GRAY2)
    d.text((x+16,y+32),v,font=F(21,bold=True),fill=vcolor)
    if vsmall: d.text((x+16+tw(d,v,F(21,bold=True))+8,y+41),vsmall,font=F(12),fill=GRAY)

def footer(d,left,right):
    y=662; d.line([54,y-12,W-54,y-12],fill=(60,70,88),width=1)
    d.text((54,y),left,font=F(12.5),fill=GRAY2)
    d.text((W-54-tw(d,right,F(12.5,bold=True)),y),right,font=F(12.5,bold=True),fill=GRAY)

def save(img,name):
    p=OUT/name; img.save(p); print("OK",name,p.stat().st_size//1024,"KB")

def img1():
    img=bg_base()
    d,_=header(img,"SISTEMAS REALES  ·  n8n PARA HOSTELERÍA",
        [[("Sabes lo que ",WHITE),("factura",WHITE),(" tu cocina.",WHITE)],
         [("¿Sabes lo que te ",WHITE),("cuesta cada plato HOY?",CYAN)]],
        "Food Cost diario · Menu Engineering · Control de desperdicio. Todo por Telegram.")
    px,py,pw,ph=54,268,700,360
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"LO QUE TE LLEGA AL MÓVIL",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+48,22,[
        ('red',"Solomillo al whisky",F(15,bold=True),WHITE,30),
        (None,"Food cost 41,2 %   ·   tu aviso: 35 %",F(14,mono=True),RED,26),
        (None,"Se está comiendo tu margen.",F(13),GRAY,28),
        (None,"Compras a 9,80 €/kg · merma limpieza 18 % · cocción 20 %",F(12.5,mono=True),MONO_C,26),
        (None,"para servir 220 g hay que comprar 335 g",F(13,mono=True),GRAY,34),
        ('amber',"Tarta de queso con trufa: INCOMPLETO",F(15,bold=True),AMBER,28),
        (None,"Falta el precio de 1 ingrediente. No se calcula:",F(13),GRAY,24),
        (None,"un dato inventado es peor que ninguno.",F(13,bold=True),WHITE,24),
    ])
    cx,cw=786,440
    card(d,cx,268,cw,74,"LAS DOS MERMAS","Encadenadas","limpieza x cocción")
    card(d,cx,352,cw,74,"NODOS REALES","31","en 3 workflows")
    card(d,cx,436,cw,74,"SE INSTALA TOCANDO","1 nodo","el nodo CONFIG")
    sello(d,cx,520,cw)
    footer(d,"Los 3 comparten la misma hoja: es un sistema, no 3 cosas sueltas","Alberto Landa · 25 años en hostelería · 10 al frente de un mesón")
    save(img,"01-portada-pack.png")

def img2():
    img=bg_base()
    d,_=header(img,"MÓDULO 1  ·  RADAR DE FOOD COST DIARIO",
        [[("Cada mañana, el ",WHITE),("semáforo",CYAN),(" de tus platos",WHITE)],
         [("en tu Telegram.",WHITE)]],
        "Recalcula el coste de materia prima y te avisa de qué plato se salió del margen.")
    px,py,pw,ph=54,268,720,360
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"EL MENSAJE DE LAS 8:00",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+48,22,[
        (None,"Mesón El Roble — coste de carta",F(15,bold=True),WHITE,26),
        (None,"4 platos · food cost medio 23,8 % (objetivo 30 %)",F(13,mono=True),GRAY,32),
        ('red',"Croquetas de jamón (6 ud)",F(15,bold=True),RED,26),
        (None,"food cost 35,5 % · coste 4,04 € · PVP 12,50 €",F(13,mono=True),MONO_C,24),
        (None,"margen 7,32 € → subirlo a 14,81 € para el 30 %",F(13,mono=True),GRAY,32),
        ('black',"Tarta de queso con trufa",F(15,bold=True),AMBER,26),
        (None,"No puedo calcularlo: falta el precio de Trufa negra.",F(12.5,mono=True),GRAY,32),
        ('green',"El que mejor va: Ensaladilla rusa (15,2 %)",F(14,bold=True),GREEN,24),
    ])
    cx,cw=806,420
    card(d,cx,268,cw,74,"SI FALTA UN PRECIO","No inventa","sale INCOMPLETO",vcolor=AMBER)
    card(d,cx,352,cw,74,"EL MARGEN VA","Sin IVA","ese 10% es de Hacienda")
    card(d,cx,436,cw,74,"TAMBIÉN A DEMANDA","/coste","cuando quieras",vcolor=CYAN)
    sello(d,cx,520,cw)
    footer(d,"Si todo está en objetivo, te dice una línea y ya. No da la brasa.","Alberto Landa · mesón en Madrid · 4,7 estrellas")
    save(img,"02-modulo1-alerta.png")

def img3():
    img=bg_base()
    d,_=header(img,"MÓDULO 1  ·  POR QUÉ TU EXCEL TE MIENTE",
        [[("Son ",WHITE),("dos mermas",CYAN),(", y se encadenan.",WHITE)]],
        "Perder al limpiar y perder al cocinar no es lo mismo. Se multiplican una tras otra.")
    px,py,pw=54,250,720
    rows=[("Solomillo al whisky","",WHITE,True),
          ("Sirves en el plato","0,220 kg",WHITE,False),
          ("Necesitas ya limpio   (-20 % al cocinar)","0,275 kg",GRAY,False),
          ("Tienes que COMPRAR   (-18 % al limpiar)","0,335 kg",CYAN,True),
          ("Coste real","3,29 €",GREEN,True),
          ("Con una sola merma del 18 % saldría","2,63 €",GRAY,False),
          ("Error: te quedas corto un","25 %",RED,True)]
    ry,rh=py,50
    for i,(k,v,c,b) in enumerate(rows):
        fill=PANEL if i==0 else (CARD if i%2 else (18,24,36))
        rrect(d,[px,ry,px+pw,ry+rh],8 if i in(0,6) else 0,fill=fill)
        d.text((px+20,ry+15),k,font=F(16,bold=b),fill=c)
        d.text((px+pw-24-tw(d,v,F(18,bold=True)),ry+13),v,font=F(18,bold=True),fill=c); ry+=rh
    cx,cw=806,420
    card(d,cx,250,cw,96,"LA HOJA TIENE DOS COLUMNAS","limpieza","x cocción",vcolor=CYAN)
    d.text((cx+16,250+66),"merma_limpieza_pct · merma_coccion_pct",font=F(11.5,mono=True),fill=GRAY)
    card(d,cx,358,cw,96,"Y LA MERMA SE","DIVIDE","no se multiplica")
    d.text((cx+16,358+66),"servir 220 g mermando 18 % = comprar 268 g",font=F(11,mono=True),fill=GRAY)
    rrect(d,[cx,466,cx+cw,466+90],11,fill=(16,34,30),outline=(30,70,60),width=1)
    d.text((cx+16,466+14),"Este fallo lo cazó una auditoría",font=F(13,bold=True),fill=GREEN)
    d.text((cx+16,466+36),"externa antes de venderlo. Estaba",font=F(13),fill=GRAY)
    d.text((cx+16,466+56),"en la v1. Ahora no.",font=F(13),fill=GRAY)
    footer(d,"El escandallo que solo usa una merma te miente a tu favor: la peor forma de mentir.","Sistemas Reales")
    save(img,"03-modulo1-doble-merma.png")

def img4():
    img=bg_base()
    d,_=header(img,"MÓDULO 2  ·  MENU ENGINEERING",
        [[("Qué plato ",WHITE),("sobra",CYAN),(" en tu carta.",WHITE)]],
        "Cruza cuánto se vende cada plato con cuánto deja. Matriz de Kasavana & Smith (1982).")
    mx,my,cell,gap=54,258,340,16
    quad=[("ESTRELLA","se vende y deja","No lo toques",GREEN,0,0),
          ("VACA LECHERA","se vende, deja poco","Sube el precio",AMBER,1,0),
          ("PUZZLE","deja, nadie lo pide","Empújalo desde la sala",CYAN,0,1),
          ("PERRO","ni se vende ni deja","Fuera de la carta",RED,1,1)]
    for tit,sub,act,col,cxi,cyi in quad:
        x=mx+cxi*(cell+gap); yq=my+cyi*(cell//2+gap); h=cell//2
        rrect(d,[x,yq,x+cell,yq+h],12,fill=CARD,outline=col,width=2)
        dot(d,x+18,yq+27,col,r=8)
        d.text((x+38,yq+16),tit,font=F(19,bold=True),fill=col)
        d.text((x+18,yq+48),sub,font=F(13),fill=GRAY)
        d.text((x+18,yq+78),"-> "+act,font=F(14,bold=True),fill=WHITE)
    px,pw,py,ph=786,440,258,336
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+20,py+16),"LO QUE TE LLEGA EL LUNES",font=F(11,bold=True),fill=GRAY2)
    block(d,px,py+42,20,[
        (None,"9 platos · 1616 servidos",F(14,bold=True),WHITE,22),
        (None,"margen medio 7,55 €/plato (ponderado)",F(12,mono=True),GRAY,30),
        ('red',"FUERA (2): Tabla de quesos, 22 uds",F(12.5,mono=True),RED,26),
        ('amber',"SUBIR PRECIO (4): Croquetas, 420 uds",F(12.5,mono=True),AMBER,26),
        ('cyan',"EMPUJAR (2): Rabo de toro, 95 uds",F(12.5,mono=True),CYAN,26),
        ('green',"NO TOCAR (1): Solomillo, 180 uds",F(12.5,mono=True),GREEN,32),
        (None,"Rabo de toro deja 11 €/plato y solo lo",F(12.5),GRAY,22),
        (None,"piden 95 veces. Ese no se quita:",F(12.5),GRAY,22),
        (None,"ese se empuja.",F(13,bold=True),WHITE,22),
    ])
    footer(d,"El listón de popularidad es el 70 % del reparto, no la media plana. Si no, matas el plato que no es.","Alberto Landa · 25 años en hostelería · 10 al frente de un mesón")
    save(img,"04-modulo2-matriz.png")

def img5():
    img=bg_base()
    d,_=header(img,"MÓDULO 3  ·  CONTROL DE DESPERDICIO",
        [[("Apuntarlo en ",WHITE),("5 segundos",CYAN),(". Ver el patrón el domingo.",WHITE)]],
        "El cocinero escribe una línea por Telegram. Sin app, sin usuario, con las manos mojadas.")
    px,py,pw=54,258,560
    rrect(d,[px,py,px+pw,py+92],12,fill=CARD,outline=CARD_B,width=1)
    d.text((px+18,py+14),"LO QUE ESCRIBE EL COCINERO",font=F(11,bold=True),fill=GRAY2)
    d.text((px+18,py+38),"merma 2 kg solomillo caducado",font=F(18,bold=True,mono=True),fill=CYAN)
    d.text((px+18,py+66),"5 segundos, con una mano, a media comanda.",font=F(12.5),fill=GRAY)
    iy,ih=py+108,268
    rrect(d,[px,iy,px+pw,iy+ih],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+18,iy+14),"Y EL DOMINGO TE LLEGA EL PATRÓN",font=F(11,bold=True),fill=GRAY2)
    block(d,px,iy+42,18,[
        ('red',"121,55 €   ·   2,89 % de las compras",F(15,bold=True),RED,24),
        (None,"a este ritmo son 1.459 € al año",F(12.5,mono=True),GRAY,30),
        (None,"¿POR QUÉ se tira?",F(13,bold=True),WHITE,24),
        (None,"80,55 € · caducado (4 veces)",F(13,mono=True),MONO_C,22),
        (None,"12,60 € · roto     ·     11,76 € · quemado",F(13,mono=True),MONO_C,30),
        ('warn',"Solomillo se ha tirado 4 veces.",F(13,bold=True),AMBER,24),
        (None,"Eso ya no es un accidente: es un patrón.",F(12.5),GRAY,22),
    ])
    cx,cw=646,580
    rrect(d,[cx,258,cx+cw,258+150],12,fill=(16,34,30),outline=(30,70,60),width=1)
    d.text((cx+18,258+16),"AGRUPA POR MOTIVO, NO POR PRODUCTO",font=F(12.5,bold=True),fill=GREEN)
    d.text((cx+18,258+46),"«El 66 % de lo que tiras está caducado»",font=F(15,bold=True),fill=WHITE)
    d.text((cx+18,258+74),"eso no es la cocina, son los PEDIDOS.",font=F(14),fill=GRAY)
    d.text((cx+18,258+98),"Compras de más o rotas mal el género —",font=F(13),fill=GRAY)
    d.text((cx+18,258+118),"y eso se arregla el lunes con una llamada.",font=F(13),fill=GRAY)
    card(d,cx,424,cw,74,"EL PARSER","casos reales","gramos a kilos, tildes, comas",vcolor=CYAN)
    card(d,cx,508,cw,74,"SI NO LO ENTIENDE","Pregunta","no se inventa el número")
    footer(d,"Una IA se inventaría el número. Un dato inventado es peor que ninguno.","Alberto Landa · 25 años en hostelería · 10 al frente de un mesón")
    save(img,"05-modulo3-desperdicio.png")

def img6():
    img=bg_base()
    d,_=header(img,"EL PACK COMPLETO  ·  3 SISTEMAS, UNA MISMA HOJA",
        [[("No son 3 cosas sueltas. ",WHITE),("Es un sistema.",CYAN)]],
        "Comparten la hoja de ingredientes: el coste que calcula uno lo usan los otros dos.")
    cols=[("1 · RADAR FOOD COST","Semáforo diario de margen por plato. La doble merma que tu Excel no hace.","9 nodos",CYAN),
          ("2 · MENU ENGINEERING","Qué plato mata tu carta: estrella, vaca, puzzle o perro. Cada lunes.","7 nodos",AMBER),
          ("3 · CONTROL DESPERDICIO","Merma en 5 s por Telegram. El patrón por MOTIVO cada domingo.","15 nodos",GREEN)]
    cw,gap,x=372,20,54
    for tit,desc,nod,col in cols:
        rrect(d,[x,262,x+cw,262+190],12,fill=CARD,outline=CARD_B,width=1)
        d.rectangle([x,262,x+5,262+190],fill=col)
        d.text((x+22,262+20),tit,font=F(16,bold=True),fill=col)
        line,yy="",262+54
        for w in desc.split():
            test=(line+" "+w).strip()
            if tw(d,test,F(13.5))>cw-44:
                d.text((x+22,yy),line,font=F(13.5),fill=GRAY); yy+=22; line=w
            else: line=test
        d.text((x+22,yy),line,font=F(13.5),fill=GRAY)
        d.text((x+22,262+156),nod+" reales",font=F(13,bold=True),fill=WHITE); x+=cw+gap
    fy=478
    rrect(d,[54,fy,634,fy+118],12,fill=(16,34,30),outline=(30,70,60),width=1)
    d.text((74,fy+14),"LO QUE SÍ HACE",font=F(14,bold=True),fill=GREEN)
    for i,s in enumerate(["Sin IA · sin claves de API · sin cuota mensual",
                          "Se instala tocando 1 nodo (el nodo CONFIG)",
                          "Si falta un dato, te lo dice. No lo inventa."]):
        d.text((74,fy+42+i*24),"· "+s,font=F(12.5),fill=GRAY)
    rrect(d,[654,fy,1226,fy+118],12,fill=(34,18,22),outline=(70,34,40),width=1)
    d.text((674,fy+14),"LO QUE NO ES (y lo digo antes)",font=F(14,bold=True),fill=RED)
    for i,s in enumerate(["No lee tu TPV ni tus facturas: los datos los pones tú",
                          "No es control de stock ni de coste total del local",
                          "Corre en TU n8n, con TUS cuentas gratuitas"]):
        d.text((674,fy+42+i*24),"· "+s,font=F(12.5),fill=GRAY)
    footer(d,"31 nodos reales · 3 guías paso a paso · documento «Qué pasa si falla»","Alberto Landa · 25 años en hostelería · 10 al frente de un mesón · 4,7/5 · +300 reseñas")
    save(img,"06-pack-completo.png")

for fn in (img1,img2,img3,img4,img5,img6): fn()
print("Galeria en",OUT)
