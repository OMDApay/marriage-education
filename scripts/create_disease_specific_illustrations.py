from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('/home/ubuntu/marriage-education-website/public/sexual-diseases-images')
OUT.mkdir(parents=True, exist_ok=True)
AR = '/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf'
ARB = '/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf'
font_title = ImageFont.truetype(ARB, 42)
font_sub = ImageFont.truetype(AR, 26)
font_title_latin = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
font_sub_latin = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
font_label = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 23)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 19)


def base(title, subtitle, accent):
    im = Image.new('RGB', (1200, 800), (248, 250, 252))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1200, 110), fill=accent)
    d.text((1140, 38), title, font=font_title_latin, fill='white', anchor='ra')
    d.text((1140, 83), subtitle, font=font_sub_latin, fill=(235, 245, 255), anchor='ra')
    d.text((45, 35), 'MEDICAL EDUCATION', font=font_label, fill='white')
    return im, d


def save(im, name):
    im.save(OUT / name, quality=95, optimize=True)

# 01: STI overview — pathogen families and transmission routes
im, d = base('STI overview', 'STIs • Definition and transmission', (28, 78, 121))
for x, y, col, label in [(170, 300, (229, 62, 62), 'Bacteria'), (430, 300, (122, 80, 180), 'Viruses'), (690, 300, (0, 133, 119), 'Parasites')]:
    d.ellipse((x-95, y-95, x+95, y+95), fill=(255,255,255), outline=col, width=10)
    if label == 'Bacteria':
        for dx, dy in [(-35,-15),(30,20),(5,-45)]: d.ellipse((x+dx-18,y+dy-10,x+dx+18,y+dy+10), fill=col)
    elif label == 'Viruses':
        d.ellipse((x-35,y-35,x+35,y+35), fill=col)
        for a,b in [(x-70,y),(x+70,y),(x,y-70),(x,y+70)]: d.line((x,y,a,b),fill=col,width=9)
    else:
        d.ellipse((x-28,y-55,x+28,y+55), outline=col, width=10); d.arc((x-65,y-45,x+65,y+45),20,320,fill=col,width=8)
    d.text((x, 430), label, font=font_label, fill=(25,35,45), anchor='ma')
d.line((900, 210, 900, 505), fill=(160, 174, 190), width=5)
d.text((1040, 260), 'Transmission', font=font_label, fill=(25,35,45), anchor='mm')
for y, txt in [(340,'Sexual contact'),(405,'Blood exposure'),(470,'Mother to child')]:
    d.ellipse((935,y-18,971,y+18), fill=(28,78,121)); d.line((990,y,1110,y), fill=(28,78,121), width=6); d.text((1120,y), txt, font=font_small, fill=(25,35,45), anchor='ra')
save(im,'sd-01.jpg')

# 02: Syphilis stages
im, d = base('Syphilis', 'Syphilis • Clinical stages', (109, 40, 120))
stages=[('1','Primary sore','Chancre'),('2','Skin rash','Rash'),('3','Latent stage','Latent'),('4','Late complications','Late disease')]
for i,(n,ar,en) in enumerate(stages):
    x=150+i*270
    d.rounded_rectangle((x-105,190,x+105,590),radius=22,fill='white',outline=(220,210,230),width=4)
    d.ellipse((x-48,220,x+48,316),fill=(245,230,240),outline=(109,40,120),width=6)
    if i==0: d.ellipse((x-20,252,x+20,285),fill=(190,50,70))
    elif i==1:
        for dx,dy in [(-25,-15),(22,-18),(-32,30),(25,32)]: d.ellipse((x+dx-10,270+dy-10,x+dx+10,270+dy+10),fill=(210,80,100))
    elif i==2: d.arc((x-32,242,x+32,306), 20, 320, fill=(109,40,120), width=9)
    else:
        d.line((x-28,250,x+28,310),fill=(190,50,70),width=10); d.line((x+28,250,x-28,310),fill=(190,50,70),width=10)
    d.text((x,370),n,font=font_label,fill=(109,40,120),anchor='mm'); d.text((x,445),ar,font=font_sub_latin,fill=(35,35,45),anchor='mm'); d.text((x,490),en,font=font_small,fill=(95,95,105),anchor='mm')
    if i<3: d.line((x+115,390,x+205,390),fill=(109,40,120),width=7); d.polygon([(x+205,390),(x+183,378),(x+183,402)],fill=(109,40,120))
save(im,'sd-02.jpg')

# 03: Gonorrhea and chlamydia
im, d = base('Gonorrhea & Chlamydia', 'Gonorrhea & Chlamydia • Bacterial infections', (0,105,92))
for x, title, col, shape in [(330,'Gonorrhea',(220,70,75),'gon'),(850,'Chlamydia',(0,105,92),'chla')]:
    d.ellipse((x-145,190,x+145,480), fill='white', outline=col, width=10)
    if shape=='gon':
        for dx,dy in [(-55,-45),(0,-10),(60,30),(-35,60),(50,-70)]:
            d.ellipse((x+dx-28,y:=260+dy-18,x+dx+28,260+dy+18),fill=col); d.line((x+dx-45,260+dy,x+dx-30,260+dy),fill=col,width=5); d.line((x+dx+30,260+dy,x+dx+45,260+dy),fill=col,width=5)
    else:
        for dx,dy in [(-55,-45),(10,-15),(55,40),(-25,55)]:
            d.ellipse((x+dx-24,260+dy-16,x+dx+24,260+dy+16),fill=col)
    d.text((x,535),title,font=font_title_latin,fill=col,anchor='ma')
d.rounded_rectangle((185,650,1015,720),radius=18,fill=(235,248,246),outline=(0,105,92),width=3)
d.text((600,685),'قد تكون العدوى بلا أعراض • الفحص والعلاج الطبي مهمان',font=font_sub_latin,fill=(0,75,65),anchor='mm')
save(im,'sd-03.jpg')

# 04: HIV and immune system
im, d = base('HIV infection', 'HIV • Immunity, testing and care', (183,28,28))
d.ellipse((200,200,500,500),fill='white',outline=(183,28,28),width=12)
d.text((350,350),'HIV',font=font_title_latin,fill=(183,28,28),anchor='mm')
for x,y in [(735,230),(900,330),(720,470),(980,500),(845,560)]:
    d.ellipse((x-42,y-42,x+42,y+42),fill=(239,100,100),outline=(130,20,20),width=5)
    for a,b in [(x-55,y),(x+55,y),(x,y-55),(x,y+55)]: d.line((x,y,a,b),fill=(130,20,20),width=6)
d.line((505,350,650,350),fill=(183,28,28),width=9); d.polygon([(650,350),(625,335),(625,365)],fill=(183,28,28))
d.text((350,575),'Targets CD4 immune cells',font=font_sub_latin,fill=(45,45,55),anchor='mm'); d.text((850,650),'Testing and early care protect health',font=font_sub_latin,fill=(45,45,55),anchor='mm')
save(im,'sd-04.jpg')

# 05: herpes lesions diagram
im, d = base('Genital herpes', 'Herpes simplex • Clinical outbreaks', (173,20,87))
d.ellipse((350,160,850,610),fill=(255,237,239),outline=(173,20,87),width=8)
d.arc((450,245,750,540),180,360,fill=(173,20,87),width=12)
for x,y in [(520,350),(590,315),(665,365),(620,430)]:
    d.ellipse((x-35,y-35,x+35,y+35),fill=(244,143,177),outline=(173,20,87),width=6)
    d.ellipse((x-15,y-15,x+15,y+15),fill=(255,215,220))
d.text((600,680),'Blisters or sores may occur • clinical assessment is important',font=font_sub_latin,fill=(90,25,55),anchor='mm')
save(im,'sd-05.jpg')

# 06 HPV
im, d = base('Human papillomavirus', 'HPV • Warts and prevention', (46,125,50))
d.ellipse((220,210,500,490),fill=(255,255,255),outline=(46,125,50),width=9)
for x,y in [(330,305),(390,370),(275,400)]: d.ellipse((x-22,y-22,x+22,y+22),fill=(165,214,167),outline=(46,125,50),width=5)
d.ellipse((720,190,930,490),fill=(255,240,245),outline=(46,125,50),width=9)
d.arc((760,240,890,420),0,180,fill=(46,125,50),width=9); d.line((825,270,825,430),fill=(46,125,50),width=8)
d.line((510,350,670,350),fill=(46,125,50),width=9); d.polygon([(670,350),(645,335),(645,365)],fill=(46,125,50))
d.text((360,560),'Many virus types',font=font_sub_latin,fill=(35,70,40),anchor='mm'); d.text((825,560),'Vaccination and screening',font=font_sub_latin,fill=(35,70,40),anchor='mm')
save(im,'sd-06.jpg')

# 07 hepatitis B/C
im, d = base('Viral hepatitis', 'Hepatitis B/C • Blood and prevention', (239,108,0))
d.ellipse((250,190,650,540),fill=(255,218,170),outline=(239,108,0),width=10)
d.line((450,270,450,470),fill=(239,108,0),width=8); d.arc((325,220,575,500),180,360,fill=(239,108,0),width=12)
d.text((450,360),'Liver',font=font_title_latin,fill=(130,60,0),anchor='mm')
d.ellipse((850,300,980,430),fill=(255,255,255),outline=(239,108,0),width=8); d.text((915,365),'B/C',font=font_label,fill=(239,108,0),anchor='mm')
d.line((680,365,820,365),fill=(239,108,0),width=9); d.polygon([(820,365),(795,350),(795,380)],fill=(239,108,0))
d.text((600,650),'Prevention: vaccination, testing, and never sharing needles',font=font_sub_latin,fill=(95,55,15),anchor='mm')
save(im,'sd-07.jpg')

# 08 parasites
im, d = base('Parasitic infections', 'Trichomoniasis • Parasite-related infections', (69,90,100))
for x,y in [(300,300),(550,250),(800,350)]:
    d.ellipse((x-70,y-45,x+70,y+45),fill=(210,235,230),outline=(69,90,100),width=7)
    d.arc((x-50,y-30,x+50,y+30),20,320,fill=(69,90,100),width=7); d.line((x-90,y,x-125,y-25),fill=(69,90,100),width=5); d.line((x+90,y,x+125,y+25),fill=(69,90,100),width=5)
d.text((600,560),'Itching, irritation or discharge require clinical diagnosis',font=font_sub_latin,fill=(45,60,65),anchor='mm')
d.rounded_rectangle((300,620,900,700),radius=16,fill=(230,238,240),outline=(69,90,100),width=3); d.text((600,660),'Do not self-medicate • diagnosis comes first',font=font_sub_latin,fill=(45,60,65),anchor='mm')
save(im,'sd-08.jpg')

# 09 testing and prevention
im, d = base('Testing and prevention', 'Testing & Prevention • Responsible steps', (0,96,100))
for x, title in [(280,'Testing'),(600,'Prevention'),(920,'Follow-up')]:
    d.rounded_rectangle((x-120,200,x+120,500),radius=24,fill='white',outline=(0,96,100),width=7)
    d.ellipse((x-55,250,x+55,360),outline=(0,96,100),width=8)
    d.line((x-25,305,x-5,330),fill=(0,96,100),width=8); d.line((x-5,330,x+45,275),fill=(0,96,100),width=8)
    d.text((x,430),title,font=font_title_latin,fill=(0,75,75),anchor='mm')
d.text((600,640),'A clinician selects testing according to health history and exposure risk',font=font_sub_latin,fill=(35,65,65),anchor='mm')
save(im,'sd-09.jpg')

# 10 doctor privacy
im, d = base('When to seek medical care', 'Clinical care • Privacy and support', (63,81,181))
d.ellipse((360,175,520,335),fill=(255,220,190),outline=(63,81,181),width=6); d.rectangle((330,330,550,560),fill=(190,205,245),outline=(63,81,181),width=6); d.rectangle((370,235,510,285),fill='white')
d.ellipse((700,200,850,350),fill=(255,220,190),outline=(63,81,181),width=6); d.rectangle((675,345,875,560),fill=(220,230,250),outline=(63,81,181),width=6)
d.line((550,410,675,410),fill=(63,81,181),width=9); d.polygon([(675,410),(650,395),(650,425)],fill=(63,81,181))
d.rounded_rectangle((250,625,950,720),radius=18,fill=(232,236,255),outline=(63,81,181),width=3); d.text((600,672),'Sores • rash • discharge • pain • persistent burning = seek medical care',font=font_sub_latin,fill=(45,55,120),anchor='mm')
save(im,'sd-10.jpg')

# disease-specific cover reuses the overview artwork but has a dedicated title panel.
cover = Image.open(OUT / 'sd-01.jpg').copy(); d=ImageDraw.Draw(cover); d.rectangle((0,0,1200,110),fill=(28,78,121)); d.text((1140,38),'Sexual diseases',font=font_title_latin,fill='white',anchor='ra'); d.text((1140,83),'Education • Testing • Prevention • Care',font=font_sub_latin,fill=(235,245,255),anchor='ra'); save(cover,'cover.jpg')
print('created_specific_images=11')
