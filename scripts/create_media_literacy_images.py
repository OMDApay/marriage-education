from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('/home/ubuntu/marriage-education-website/public/porn-media-images')
OUT.mkdir(parents=True, exist_ok=True)
B = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)
S = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 23)
SM = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
items = [
 ('FILM IS NOT REAL LIFE','Performance, editing and selective scenes', (93,48,150)),
 ('EDITING HIDES THE PROCESS','Camera angles, cuts and preparation', (25,88,120)),
 ('BODIES ARE DIVERSE','Do not compare yourself with a screen', (0,115,95)),
 ('CONSENT COMES FIRST','Ask, listen and respect boundaries', (184,55,75)),
 ('EXPECTATIONS NEED REALITY','A private relationship is not a show', (185,105,25)),
 ('TALK, DO NOT IMITATE','Communication builds trust', (47,90,170)),
 ('SAFETY IS NOT A CAMERA TRICK','Hygiene and health need real care', (170,60,55)),
 ('CHECK THE SOURCE','Medical education needs reliable references', (50,110,75)),
 ('SEEK SUPPORT WHEN NEEDED','You deserve help without shame', (112,72,145)),
 ('HEALTHY INTIMACY IS PRIVATE','Knowledge, kindness and mutual choice', (35,95,115)),
]

def make(title, subtitle, col, idx):
    im=Image.new('RGB',(1200,800),(248,250,252)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1200,120),fill=col); d.text((55,38),f'{idx:02d}  MEDIA LITERACY',font=SM,fill='white'); d.text((1140,45),title,font=B,fill='white',anchor='ra'); d.text((1140,91),subtitle,font=S,fill=(235,245,255),anchor='ra')
    if idx==1:
        d.rectangle((180,240,530,510),outline=col,width=14); d.polygon([(530,300),(700,375),(530,450)],fill=col); d.rounded_rectangle((730,210,1030,540),radius=28,fill='white',outline=(150,160,180),width=6); d.rectangle((790,270,970,390),fill=(220,230,245)); d.ellipse((860,320,900,360),fill=col); d.line((870,440,940,440),fill=col,width=10)
    elif idx==2:
        d.rectangle((180,230,1020,520),outline=col,width=12); d.line((230,480,970,260),fill=col,width=10); d.line((230,260,970,480),fill=(210,80,90),width=10); d.text((600,590),'The final scene does not show every step',font=S,fill=(35,45,55),anchor='mm')
    elif idx==3:
        for x,h,c in [(280,180,(240,170,165)),(520,250,(180,205,235)),(760,210,(170,220,190))]: d.ellipse((x-65,300-h//2,x+65,300+h//2),fill=c,outline=col,width=6); d.rectangle((x-80,410,x+80,570),fill=c,outline=col,width=6)
        d.text((600,650),'Different bodies • different experiences',font=S,fill=(35,45,55),anchor='mm')
    elif idx==4:
        for x in [330,870]: d.ellipse((x-75,230,x+75,380),fill=(255,220,190),outline=col,width=6); d.rectangle((x-100,380,x+100,570),fill=(215,225,245),outline=col,width=6)
        d.line((480,400,720,400),fill=col,width=9); d.text((600,650),'Ask • listen • respect • stop when needed',font=S,fill=(35,45,55),anchor='mm')
    elif idx==5:
        d.rounded_rectangle((180,220,550,520),radius=26,fill=(255,240,225),outline=col,width=8); d.rounded_rectangle((650,220,1020,520),radius=26,fill=(225,245,240),outline=col,width=8); d.text((365,360),'SCREEN',font=B,fill=col,anchor='mm'); d.text((835,360),'REAL LIFE',font=B,fill=col,anchor='mm'); d.text((600,650),'Reality includes feelings, pauses and mutual care',font=S,fill=(35,45,55),anchor='mm')
    elif idx==6:
        for x,y in [(290,300),(600,240),(900,330)]: d.ellipse((x-55,y-55,x+55,y+55),outline=col,width=8); d.line((x-35,y,x+35,y),fill=col,width=8); d.line((x,y-35,x,y+35),fill=col,width=8)
        d.text((600,650),'A scene cannot replace health guidance',font=S,fill=(35,45,55),anchor='mm')
    elif idx==7:
        d.rectangle((250,230,430,500),fill=(220,235,245),outline=col,width=8); d.ellipse((290,290,390,390),outline=col,width=8); d.line((330,340,360,370),fill=col,width=8); d.line((360,370,420,300),fill=col,width=8); d.rectangle((720,250,900,470),fill=(240,250,240),outline=col,width=8); d.text((810,360),'SOURCE',font=S,fill=col,anchor='mm'); d.line((480,360,680,360),fill=col,width=8); d.polygon([(680,360),(650,345),(650,375)],fill=col)
    elif idx==8:
        d.ellipse((300,230,450,380),fill=(255,220,190),outline=col,width=6); d.rectangle((270,380,480,570),fill=(210,220,250),outline=col,width=6); d.ellipse((750,230,900,380),fill=(255,220,190),outline=col,width=6); d.rectangle((720,380,930,570),fill=(225,235,250),outline=col,width=6); d.line((480,430,720,430),fill=col,width=9); d.text((600,650),'Asking for help is a strength',font=S,fill=(35,45,55),anchor='mm')
    elif idx==9:
        d.rectangle((190,230,1010,510),fill=(235,242,250),outline=col,width=8); d.line((300,430,900,430),fill=col,width=8); d.line((380,360,500,420),fill=col,width=8); d.line((820,360,700,420),fill=col,width=8); d.text((600,650),'Reliable information • privacy • support',font=S,fill=(35,45,55),anchor='mm')
    elif idx==10:
        d.ellipse((300,250,450,400),fill=(255,220,190),outline=col,width=6); d.ellipse((750,250,900,400),fill=(255,220,190),outline=col,width=6); d.rectangle((270,400,480,590),fill=(215,230,250),outline=col,width=6); d.rectangle((720,400,930,590),fill=(225,245,235),outline=col,width=6); d.line((480,470,720,470),fill=col,width=9); d.text((600,650),'Mutual choice, kindness and privacy',font=S,fill=(35,45,55),anchor='mm')
    im.save(OUT/f'pm-{idx:02d}.jpg',quality=95,optimize=True)

for i,(a,b,c) in enumerate(items,1): make(a,b,c,i)
# cover uses a dedicated title and the same non-explicit visual style
cover=Image.new('RGB',(1200,800),(245,247,252)); d=ImageDraw.Draw(cover); d.rectangle((0,0,1200,180),fill=(93,48,150)); d.text((600,70),'MEDIA LITERACY',font=B,fill='white',anchor='mm'); d.text((600,135),'Do not mistake a performance for a guide to marriage',font=S,fill=(235,225,250),anchor='mm'); d.rectangle((250,260,950,540),fill='white',outline=(93,48,150),width=10); d.line((600,280,600,520),fill=(93,48,150),width=9); d.text((420,400),'FILM',font=B,fill=(93,48,150),anchor='mm'); d.text((780,400),'REALITY',font=B,fill=(93,48,150),anchor='mm'); d.text((600,680),'Knowledge • consent • communication',font=S,fill=(45,50,60),anchor='mm'); cover.save(OUT/'cover.jpg',quality=95,optimize=True)
print('created=',len(items)+1)
