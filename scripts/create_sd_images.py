from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path('/home/ubuntu/marriage-education-website/public/sexual-diseases-images')
root.mkdir(parents=True, exist_ok=True)
font_bold = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf', 42)
font_regular = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf', 25)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
labels = [
    'مقدمة: فهم العدوى', 'الزهري', 'السيلان والكلاميديا', 'فيروس HIV', 'الهربس',
    'فيروس HPV', 'التهاب الكبد', 'العدوى الطفيلية', 'الفحص والوقاية', 'الاستشارة والخصوصية'
]
palettes = [
    ((13, 71, 161), (100, 181, 246)), ((109, 40, 217), (196, 181, 253)),
    ((0, 105, 92), (128, 203, 196)), ((183, 28, 28), (239, 154, 154)),
    ((173, 20, 87), (244, 143, 177)), ((46, 125, 50), (165, 214, 167)),
    ((239, 108, 0), (255, 204, 128)), ((69, 90, 100), (176, 190, 197)),
    ((0, 96, 100), (128, 222, 234)), ((63, 81, 181), (159, 168, 218)),
]

def make_image(index, label, filename):
    c1, c2 = palettes[index]
    im = Image.new('RGB', (1000, 650), c1)
    d = ImageDraw.Draw(im)
    for x in range(-100, 1100, 70):
        d.polygon([(x, 0), (x + 330, 0), (x - 20, 650), (x - 350, 650)], fill=tuple(min(255, int(c1[i] * .58 + c2[i] * .42)) for i in range(3)))
    # Abstract medical symbols: shield, microscope, test tube, cross, network, DNA, liver, parasite, checklist, consultation.
    if index == 0:
        d.ellipse((355, 100, 645, 390), outline='white', width=14)
        d.line((500, 145, 500, 350), fill='white', width=12)
        d.line((420, 250, 580, 250), fill='white', width=12)
    elif index == 1:
        d.polygon([(500, 95), (670, 160), (640, 350), (500, 470), (360, 350), (330, 160)], outline='white', width=14)
        d.line((500, 180, 500, 365), fill='white', width=11)
        d.line((430, 270, 570, 270), fill='white', width=11)
    elif index == 2:
        d.ellipse((330, 160, 550, 380), outline='white', width=12)
        d.ellipse((500, 250, 720, 470), outline='white', width=12)
        d.line((475, 270, 575, 370), fill='white', width=10)
    elif index == 3:
        d.circle = None
        d.ellipse((390, 110, 610, 330), outline='white', width=12)
        d.line((500, 330, 500, 475), fill='white', width=12)
        d.line((430, 395, 570, 395), fill='white', width=12)
        d.line((455, 475, 545, 475), fill='white', width=12)
    elif index == 4:
        d.ellipse((360, 140, 640, 420), outline='white', width=12)
        d.arc((405, 185, 595, 375), 20, 320, fill=c2, width=20)
        d.ellipse((485, 265, 515, 295), fill='white')
    elif index == 5:
        d.line((390, 130, 610, 470), fill='white', width=10)
        d.line((610, 130, 390, 470), fill='white', width=10)
        for y in range(160, 451, 70):
            d.ellipse((370, y-15, 410, y+25), fill=c2)
            d.ellipse((590, y-15, 630, y+25), fill=c2)
    elif index == 6:
        d.ellipse((360, 180, 640, 440), fill=c2, outline='white', width=8)
        d.arc((420, 120, 580, 300), 20, 160, fill='white', width=12)
        d.line((500, 300, 500, 500), fill='white', width=12)
    elif index == 7:
        for x, y, r in [(380, 220, 45), (500, 140, 38), (620, 220, 45), (440, 390, 40), (560, 390, 40)]:
            d.ellipse((x-r, y-r, x+r, y+r), outline='white', width=10)
        for a, b in [((380,220),(500,140)),((500,140),(620,220)),((380,220),(440,390)),((620,220),(560,390)),((440,390),(560,390))]:
            d.line((*a, *b), fill=c2, width=9)
    elif index == 8:
        d.rounded_rectangle((330, 125, 670, 475), radius=28, outline='white', width=10)
        for y in [190, 285, 380]:
            d.ellipse((375, y-15, 405, y+15), fill=c2)
            d.line((435, y, 610, y), fill='white', width=10)
    else:
        d.ellipse((330, 150, 500, 320), outline='white', width=10)
        d.ellipse((500, 150, 670, 320), outline='white', width=10)
        d.line((500, 320, 500, 440), fill='white', width=10)
        d.arc((390, 330, 610, 570), 180, 360, fill='white', width=12)
    d.rounded_rectangle((55, 520, 945, 615), radius=18, fill=(0, 0, 0))
    d.text((500, 568), label, font=font_bold, fill='white', anchor='mm')
    d.text((55, 45), f'EDUCATIONAL • {index + 1:02d}', font=font_small, fill='white')
    im.save(root / filename, quality=93, optimize=True)

for i, label in enumerate(labels):
    make_image(i, label, f'sd-{i+1:02d}.jpg')
make_image(0, 'الأمراض الجنسية: التوعية والوقاية', 'cover.jpg')
print('created=', len(labels) + 1)
