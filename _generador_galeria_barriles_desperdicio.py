# -*- coding: utf-8 -*-
"""Galeria Barriles + Desperdicio — estilo Sistemas Reales, 1280x720, Pillow puro.
Emojis dibujados a mano (DejaVu no los trae). Cifras reales de las guias."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1280, 720
BG=(10,14,24); PANEL=(15,21,32); PANEL_B=(34,48,74); CARD=(23,28,40); CARD_B=(42,50,68)
CYAN=(56,189,248); RED=(244,63,94); GREEN=(52,211,153); AMBER=(251,191,36)
WHITE=(255,255,255); GRAY=(148,163,184); GRAY2=(100,116,139); MONO_C=(203,213,225)
FD="/usr/share/fonts/truetype/dejavu"
def F(sz,bold=False,mono=False):
    f=("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf") if mono else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(f"{FD}/{f}",int(sz))
def bg_base():
    img=Image.new("RGB",(W,H),BG); glow=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(glow)
    gd.ellipse([820,-260,1500,320],fill=(20,40,60)); gd.ellipse([-260,460,360,1000],fill=(40,20,30))
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
def card(d,x,y,w,h,k,v,vcolor=WHITE):
    rrect(d,[x,y,x+w,y+h],11,fill=CARD,outline=CARD_B,width=1)
    d.text((x+16,y+13),k,font=F(11,bold=True),fill=GRAY2)
    d.text((x+16,y+32),v,font=F(21,bold=True),fill=vcolor)
def footer(d,left,right):
    y=662; d.line([54,y-12,W-54,y-12],fill=(60,70,88),width=1)
    d.text((54,y),left,font=F(12.5),fill=GRAY2)
    d.text((W-54-tw(d,right,F(12.5,bold=True)),y),right,font=F(12.5,bold=True),fill=GRAY)

# ---------------- BARRILES ----------------
def bar_out(name):
    return Path("/sessions/fervent-optimistic-newton/mnt/CEREBRO-DIGITAL-ALBERTO/_recursos/_assets-publicos/control-barriles-bar/galeria")/name
MARCA_B="SISTEMAS REALES  ·  n8n PARA HOSTELERÍA"
FOOT_B="Sistemas Reales · Control de barriles"

def b1():
    img=bg_base()
    d,_=header(img,MARCA_B,
        [[("\"Los barriles duran menos",WHITE)],[("de lo que deberían.\"",WHITE)]],
        "Deja de intuirlo. Mira cuántos euros se te van en CADA barril.")
    px,py,pw,ph=54,250,760,300
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"LO QUE TE LLEGA AL MÓVIL CUANDO SE ACABA UN BARRIL",font=F(11,bold=True),fill=GRAY2)
    d.text((px+22,py+52),"SE HAN PERDIDO",font=F(16),fill=GRAY)
    d.text((px+22,py+78),"25,96 €",font=F(64,bold=True),fill=RED)
    d.text((px+22,py+160),"en este barril de Estrella Galicia (duró 4 días)",font=F(16),fill=GRAY)
    d.text((px+22,py+196),"Rendimiento 90,07 %  ·  cada caña te cuesta 0,77 € en vez de 0,64 €",font=F(15,bold=True),fill=AMBER)
    card(d,900,270,326,84,"CÓMO SE APUNTA","Telegram",CYAN)
    card(d,900,368,326,84,"INTELIGENCIA","Sin IA",GREEN)
    sello(d,900,466,326,"59 € · pago único, sin cuota")
    footer(d,FOOT_B,"1 / 6"); img.save(bar_out("gal-1-portada.png")); print("bar1")

def b2():
    img=bg_base()
    d,_=header(img,MARCA_B,[[("El mensaje que te llega,",WHITE)],[("con los ",WHITE),("euros de verdad",CYAN),(".",WHITE)]],
        "No 'rendimiento' en abstracto: lo que has perdido, en euros, por barril.")
    px,py,pw,ph=54,250,1172,300
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+24,py+20),"ESTRELLA GALICIA  ·  cerrado, duró 4 días",font=F(15,bold=True),fill=AMBER)
    rows=[("Debía dar","29,7 L  =  118 cañas  =  261,36 €",WHITE),
          ("Ha dado","26,75 L  =  107 cañas",WHITE),
          ("Rendimiento","90,07 %",AMBER),
          ("Perdido de verdad","25,96 €",RED)]
    yy=py+62
    for k,v,c in rows:
        d.text((px+24,yy),k,font=F(15),fill=GRAY); d.text((px+300,yy),v,font=F(17,bold=True),fill=c); yy+=44
    d.text((px+24,yy+6),"Ya descontado: 6 invitadas · 4 de personal · 0,3 L de purga — decisiones tuyas, no fugas.",font=F(13),fill=GRAY2)
    footer(d,FOOT_B,"2 / 6"); img.save(bar_out("gal-2-informe.png")); print("bar2")

def b3():
    img=bg_base()
    d,_=header(img,MARCA_B,[[("Tres mensajes. ",WHITE),("Eso es todo.",CYAN)]],
        "El encargado escribe en Telegram. Sin apps nuevas, sin formación.")
    steps=[("1","Al pinchar el barril","barril rubia",CYAN),
           ("2","Al cerrar el turno","cañas 85   invitadas 6   personal 4",GREEN),
           ("3","Cuando se acaba","vacio rubia",AMBER)]
    y=270
    for n,label,cmd,c in steps:
        rrect(d,[54,y,1226,y+108],14,fill=PANEL,outline=PANEL_B,width=1)
        rrect(d,[78,y+34,110,y+74],9,fill=c); d.text((88,y+40),n,font=F(22,bold=True),fill=(10,14,24))
        d.text((130,y+22),label,font=F(15,bold=True),fill=GRAY)
        rrect(d,[130,y+50,700,y+88],9,fill=(18,26,40),outline=(34,48,74),width=1)
        d.text((146,y+59),cmd,font=F(16,mono=True),fill=MONO_C)
        y+=124
    footer(d,FOOT_B,"3 / 6"); img.save(bar_out("gal-3-como-se-usa.png")); print("bar3")

def b4():
    img=bg_base()
    d,_=header(img,MARCA_B,[[("El coste real de cada caña,",WHITE)],[("cara a cara con el teórico.",CYAN)]],
        "La diferencia entre lo que crees que ganas y lo que ganas de verdad.")
    card(d,54,268,380,150,"COSTE TEÓRICO POR CAÑA","0,64 €",GREEN)
    card(d,447,268,380,150,"COSTE REAL POR CAÑA","0,77 €",RED)
    card(d,840,268,386,150,"RENDIMIENTO DEL BARRIL","90,07 %",AMBER)
    px,py,pw,ph=54,442,1172,150
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"LO QUE EL SISTEMA DESCUENTA ANTES DE HABLAR DE 'PÉRDIDA'",font=F(11,bold=True),fill=GRAY2)
    d.text((px+22,py+50),"6 cañas invitadas = 13,20 €   ·   4 de personal = 8,80 €   ·   0,3 L de purga",font=F(16,bold=True),fill=WHITE)
    d.text((px+22,py+92),"Son decisiones tuyas, no fugas. El sistema solo te enseña lo que de verdad se escapa.",font=F(14),fill=GRAY)
    footer(d,FOOT_B,"4 / 6"); img.save(bar_out("gal-4-desglose.png")); print("bar4")

def b5():
    img=bg_base()
    d,_=header(img,MARCA_B,[[("Primero mides tu vaso.",WHITE)],[("Si no, ",WHITE),("todo es mentira",AMBER),(".",WHITE)]],
        "La honestidad que hace que te creas el número. Nada de humo.")
    px,py,pw,ph=54,258,1172,300
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    pts=[("El sistema no adivina el tamaño de tu caña: se lo dices tú, una vez.",WHITE),
         ("Con eso calcula cuántas cañas 'debía' dar el barril y las compara con las reales.",GRAY),
         ("Por eso el número es tuyo, no un dato de catálogo que no encaja con tu barra.",GRAY),
         ("Cinco minutos de calibrado = un informe en el que puedes confiar para siempre.",WHITE)]
    yy=py+40
    for t,c in pts:
        dot(d,px+24,yy+12,CYAN,r=6); d.text((px+48,yy),t,font=F(17,bold=True if c==WHITE else False),fill=c); yy+=58
    footer(d,FOOT_B,"5 / 6"); img.save(bar_out("gal-5-mide-vaso.png")); print("bar5")

def b6():
    img=bg_base()
    d,_=header(img,MARCA_B,[[("Se instala una vez.",WHITE)],[("Y ya ",WHITE),("no paga cuota nunca",GREEN),(".",WHITE)]],
        "Corre en tu propio n8n. Tú eres el dueño del sistema.")
    items=[("Workflow de n8n listo","Import from File, rellenas 2 datos y activar"),
           ("Guía paso a paso en español","De cero a funcionando, con ejemplos reales"),
           ("Manual 'Qué pasa si falla'","Los 6 fallos típicos y cómo resolverlos solo")]
    y=262
    for k,v in items:
        rrect(d,[54,y,820,y+92],12,fill=CARD,outline=CARD_B,width=1)
        dot(d,80,y+46,GREEN,r=8); d.text((104,y+18),k,font=F(18,bold=True),fill=WHITE)
        d.text((104,y+50),v,font=F(14),fill=GRAY); y+=106
    sello(d,850,262,376,"59 € · pago único");
    card(d,850,340,376,120,"LO QUE AHORRAS EN 1 BARRIL MALO","25,96 €",RED)
    d.text((850,472),"Con recuperar un barril al mes,",font=F(14),fill=GRAY)
    d.text((850,494),"el sistema ya se ha pagado.",font=F(14,bold=True),fill=WHITE)
    footer(d,FOOT_B,"6 / 6"); img.save(bar_out("gal-6-que-incluye.png")); print("bar6")

# ---------------- DESPERDICIO ----------------
def des_out(name):
    return Path("/sessions/fervent-optimistic-newton/mnt/CEREBRO-DIGITAL-ALBERTO/_recursos/_assets-publicos/control-desperdicio-gratis/galeria")/name
MARCA_D="SISTEMAS REALES  ·  n8n PARA HOSTELERÍA"
FOOT_D="Sistemas Reales · Control de desperdicio (GRATIS)"

def d1():
    img=bg_base()
    d,_=header(img,MARCA_D,[[("Todo el mundo sabe",WHITE)],[("que se ",WHITE),("tira comida",RED),(".",WHITE)]],
        "Nadie sabe cuánta, de qué, ni por qué. Así que no cambia nada.")
    px,py,pw,ph=54,250,760,300
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"LO QUE ESTE SISTEMA TE DICE EL DOMINGO",font=F(11,bold=True),fill=GRAY2)
    d.text((px+22,py+52),"El",font=F(16),fill=GRAY)
    d.text((px+62,py+44),"66 %",font=F(56,bold=True),fill=AMBER)
    d.text((px+22,py+120),"de lo que tiras está CADUCADO",font=F(22,bold=True),fill=WHITE)
    d.text((px+22,py+164),"Eso no es un problema de cocina.",font=F(16),fill=GRAY)
    d.text((px+22,py+190),"Es un problema de PEDIDOS — y se arregla el lunes.",font=F(16,bold=True),fill=CYAN)
    card(d,900,270,326,84,"CÓMO SE APUNTA","Telegram",CYAN)
    card(d,900,368,326,84,"INTELIGENCIA","Sin IA",GREEN)
    sello(d,900,466,326,"GRATIS · descarga y pruébalo")
    footer(d,FOOT_D,"1 / 6"); img.save(des_out("gal-1-portada.png")); print("des1")

def d2():
    img=bg_base()
    d,_=header(img,MARCA_D,[[("No te dice ",WHITE),("cuánto",GRAY),(" tiras.",WHITE)],[("Te dice ",WHITE),("por qué",CYAN),(".",WHITE)]],
        "\"Has tirado 121 €\" no sirve de nada. El motivo sí se puede corregir.")
    px,py,pw,ph=54,258,570,300
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=(90,40,50),width=1)
    d.text((px+22,py+18),"LO INÚTIL",font=F(11,bold=True),fill=GRAY2)
    d.text((px+22,py+52),"\"Has tirado 121 €\"",font=F(24,bold=True),fill=GRAY)
    d.text((px+22,py+100),"No puedes hacer nada con eso.",font=F(15),fill=GRAY2)
    px2=654
    rrect(d,[px2,py,px2+572,py+300],14,fill=PANEL,outline=(30,70,60),width=1)
    d.text((px2+22,py+18),"LO QUE CAMBIA EL LUNES",font=F(11,bold=True),fill=GRAY2)
    d.text((px2+22,py+52),"\"El 66 % está caducado\"",font=F(22,bold=True),fill=GREEN)
    d.text((px2+22,py+100),"Compras de más o rotas mal el género.",font=F(15),fill=WHITE)
    d.text((px2+22,py+130),"Una llamada al proveedor y arreglado.",font=F(15),fill=WHITE)
    d.text((px2+22,py+186),"Y avisa de patrones:",font=F(14),fill=GRAY)
    d.text((px2+22,py+212),"el solomillo se ha tirado 4 veces,",font=F(15,bold=True),fill=AMBER)
    d.text((px2+22,py+238),"eso ya no es un accidente.",font=F(15,bold=True),fill=AMBER)
    footer(d,FOOT_D,"2 / 6"); img.save(des_out("gal-2-por-que.png")); print("des2")

def d3():
    img=bg_base()
    d,_=header(img,MARCA_D,[[("Cinco segundos. ",CYAN),("Con una mano.",WHITE)]],
        "A media comanda, sin quitarse el guante. Todo lo demás lo perdona.")
    px,py,pw,ph=54,258,1172,120
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+22),"LO QUE ESCRIBES",font=F(11,bold=True),fill=GRAY2)
    rrect(d,[px+22,py+50,px+560,py+92],9,fill=(18,26,40),outline=(34,48,74),width=1)
    d.text((px+38,py+59),"merma 2 kg solomillo caducado",font=F(17,mono=True),fill=MONO_C)
    d.text((px+610,py+38),"->",font=F(30,bold=True),fill=CYAN)
    d.text((px+680,py+40),"2 kg de Solomillo · caducado",font=F(18,bold=True),fill=GREEN)
    rows=[("tirar 1,5 kg merluza malo","1,5 kg de Merluza · malo"),
          ("merma 500 g trufa negra caducada","0,5 kg de Trufa negra · caducado"),
          ("rotura 3 ud vino tinto roto","3 ud de Vino tinto · roto")]
    y=py+150
    for a,b in rows:
        rrect(d,[54,y,1226,y+58],11,fill=CARD,outline=CARD_B,width=1)
        d.text((78,y+18),a,font=F(15,mono=True),fill=MONO_C)
        d.text((700,y+16),"->  "+b,font=F(15,bold=True),fill=WHITE); y+=70
    footer(d,FOOT_D,"3 / 6"); img.save(des_out("gal-3-como-se-escribe.png")); print("des3")

def d4():
    img=bg_base()
    d,_=header(img,MARCA_D,[[("Agrupa por ",WHITE),("MOTIVO",CYAN),(",",WHITE)],[("no por producto.",WHITE)]],
        "El motivo es lo único que puedes corregir. Por eso manda el informe.")
    px,py,pw,ph=54,258,1172,300
    rrect(d,[px,py,px+pw,py+ph],14,fill=PANEL,outline=PANEL_B,width=1)
    d.text((px+22,py+18),"INFORME DEL DOMINGO 20:00  ·  AGRUPADO POR MOTIVO",font=F(11,bold=True),fill=GRAY2)
    bars=[("Caducado",66,RED),("Mal estado",20,AMBER),("Rotura",14,GRAY)]
    y=py+60
    for k,pct,c in bars:
        d.text((px+22,y),k,font=F(16,bold=True),fill=WHITE)
        rrect(d,[px+240,y+2,px+240+int(pct*8.5),y+26],6,fill=c)
        d.text((px+240+int(pct*8.5)+12,y+2),f"{pct} %",font=F(16,bold=True),fill=c); y+=52
    d.text((px+22,y+14),"Y avisa de patrones: el solomillo tirado 4 veces ya no es casualidad.",font=F(15,bold=True),fill=AMBER)
    d.text((px+22,y+46),"También bajo demanda con  /mermas  cuando quieras.",font=F(14),fill=GRAY)
    footer(d,FOOT_D,"4 / 6"); img.save(des_out("gal-4-informe.png")); print("des4")

def d5():
    img=bg_base()
    d,_=header(img,MARCA_D,[[("La hoja de la cámara",WHITE)],[("dura ",WHITE),("nueve días",RED),(". Siempre.",WHITE)]],
        "Apuntar con las manos mojadas un viernes a las 21:30 no lo hace nadie.")
    px,py=54,258
    rrect(d,[px,py,px+570,py+300],14,fill=PANEL,outline=(90,40,50),width=1)
    d.text((px+22,py+18),"LA HOJA DE PAPEL",font=F(11,bold=True),fill=GRAY2)
    d.text((px+22,py+56),"Dura 9 días",font=F(22,bold=True),fill=GRAY)
    for i,t in enumerate(["Manos mojadas","Boli que no aparece","Nadie la lee luego"]):
        dot(d,px+30,py+118+i*44,RED,r=6); d.text((px+52,py+108+i*44),t,font=F(16),fill=GRAY)
    px2=654
    rrect(d,[px2,py,px2+572,py+300],14,fill=PANEL,outline=(30,70,60),width=1)
    d.text((px2+22,py+18),"POR TELEGRAM",font=F(11,bold=True),fill=GRAY2)
    d.text((px2+22,py+56),"El móvil ya está en el bolsillo",font=F(19,bold=True),fill=GREEN)
    for i,t in enumerate(["5 segundos por apunte","Sin apps nuevas","El domingo, el patrón solo"]):
        dot(d,px2+30,py+118+i*44,GREEN,r=6); d.text((px2+52,py+108+i*44),t,font=F(16,bold=True),fill=WHITE)
    footer(d,FOOT_D,"5 / 6"); img.save(des_out("gal-5-telegram.png")); print("des5")

def d6():
    img=bg_base()
    d,_=header(img,MARCA_D,[[("Gratis. ",GREEN),("Y tú eres el dueño",WHITE)],[("del sistema.",WHITE)]],
        "Corre en tu propio n8n. Sin cuota, sin claves, sin depender de nadie.")
    items=[("Workflow de n8n listo","Import from File, rellenas 2 datos y activar"),
           ("Guía paso a paso en español","De cero a funcionando en 10 minutos"),
           ("Manual 'Qué pasa si falla'","Los fallos típicos y cómo resolverlos solo")]
    y=262
    for k,v in items:
        rrect(d,[54,y,820,y+92],12,fill=CARD,outline=CARD_B,width=1)
        dot(d,80,y+46,GREEN,r=8); d.text((104,y+18),k,font=F(18,bold=True),fill=WHITE)
        d.text((104,y+50),v,font=F(14),fill=GRAY); y+=106
    sello(d,850,262,376,"GRATIS · sin registro de tarjeta")
    card(d,850,340,376,120,"LO QUE APRENDES EL PRIMER DOMINGO","El 66 %",AMBER)
    d.text((850,472),"Deja de tirar dinero a ciegas.",font=F(14),fill=GRAY)
    d.text((850,494),"Empieza a verlo hoy.",font=F(14,bold=True),fill=WHITE)
    footer(d,FOOT_D,"6 / 6"); img.save(des_out("gal-6-que-incluye.png")); print("des6")

for fn in [b1,b2,b3,b4,b5,b6,d1,d2,d3,d4,d5,d6]:
    fn()
print("== DONE ==")
