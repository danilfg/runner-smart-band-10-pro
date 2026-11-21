"""Deterministic, original cartoon SVG illustrations rasterized to PNG for Vela.
No external/restricted artwork is used, only handcrafted vector primitives.
"""
from pathlib import Path
from random import Random
import cairosvg
from PIL import Image
import io

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'src'/'common'
DEST.mkdir(parents=True,exist_ok=True)

def svg(w,h,content):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{content}</svg>'
def path(d,fill,stroke='#262533',sw=3):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def rect(x,y,w,h,fill,stroke='#282b35',sw=3,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def ellipse(x,y,rx,ry,fill,stroke='#282b35',sw=3):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circle(x,y,r,fill,stroke='#282b35',sw=3):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,color='#272a31',w=3):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'

def save(name,w,h,content):
 # Character PNGs are carefully authored artwork, not procedural placeholders.
 # Keep them unchanged when regenerating procedural background/prop graphics.
 if name.startswith('hero_') and (DEST/name).exists():
  print('keep character art:',name)
  return
 raw=cairosvg.svg2png(bytestring=svg(w,h,content).encode('utf8'),output_width=w,output_height=h)
 im=Image.open(io.BytesIO(raw)).convert('RGBA')
 # lossless palette works for tiny app budget without large RGBA assets
 if name.startswith('city'):
  im=im.convert('RGB').quantize(colors=96)
 else:
  im=im.quantize(colors=128)
 im.save(DEST/name,optimize=True)
 print(name, (DEST/name).stat().st_size)

# Hand-painted-looking continuous panoramas with strong outlines and small irregular details.
for layer in (0,1):
 rng=Random(715+layer)
 contents=['''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#26caef"/><stop offset="1" stop-color="#a4ecde"/></linearGradient>
  <linearGradient id="road" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#657184"/><stop offset="1" stop-color="#424958"/></linearGradient>
 </defs>''',rect(0,0,672,480,'url(#sky)','none',0)]
 for x,y in [(27,58),(246,75),(526,48)]:
  contents += [ellipse(x,y,47,15,'#fff8e7','#65bfd9',2),ellipse(x+22,y-11,32,22,'#fff8e7','#65bfd9',2),ellipse(x-10,y-8,29,20,'#fff8e7','#65bfd9',2)]
 # distant town skyline
 for i in range(15):
  x=i*52-10; y=200+rng.randint(-75,10)
  contents.append(rect(x,y,49,290-y,rng.choice(['#94bbb7','#8bb6c2','#a4afbe','#b1c4b2']), '#688f93',1))
  for row in range(int((285-y)//31)):
   for col in (0,1):
    contents.append(rect(x+8+col*21,y+12+row*30,10,15,'#f5e6a7','#7799a1',1))
 # houses
 palettes=[('#ffd46e','#db9b7c'),('#bcd8cf','#ee956b'),('#ffb89f','#f7dbb0'),('#d8d0b5','#7aaab9')]
 for i in range(4):
  x=30+i*183+rng.randint(-22,18); w=146+rng.randint(-14,15); y=220+rng.randint(-26,18)
  base,trim=palettes[(i+layer)%4]
  contents.append(rect(x,y,w,154,base,'#34313d',3))
  contents.append(path(f'M{x-10} {y+4} L{x+w/2} {y-64} L{x+w+10} {y+4} Z',trim))
  contents.append(rect(x+18,y+28,38,45,'#75cae1','#34313d',3))
  contents.append(rect(x+78,y+28,38,45,'#75cae1','#34313d',3))
  for xx in [x+37,x+97]:contents.append(line(xx,y+29,xx,y+72,'#fff0d9',3))
  contents.append(rect(x+61,y+90,35,64,'#b87870','#37323a',3))
  contents.append(circle(x+87,y+122,3,'#fce69b','#333',1))
  # cracks / bricks
  for j in range(4):
   px=x+rng.randint(4,w-5); py=y+rng.randint(14,117)
   contents.append(path(f'M{px} {py} l7 0 l3 6', 'none','#aa8179',1))
 # fence and hedges
 contents += [rect(0,362,672,20,'#c7a2a0','#34404b',2)]
 for x in range(-15,690,26):
  contents.append(path(f'M{x} 359 L{x} 313 Q{x+12} 294 {x+24} 313 L{x+24} 359 Z','#f2e7c3','#6d8076',1))
 for x in range(-20,690,74):
  contents.append(ellipse(x+31,355,51,32,'#55b95a','#2d754b',2))
  contents.append(circle(x+15,334,24,'#68cf61','#338f47',2))
  contents.append(circle(x+43,337,21,'#84df6c','#338f47',2))
  contents.append(circle(x+30,349,3,'#f89ab4','none',0))
 # sidewalk and road foreground
 contents += [rect(0,372,672,26,'#edcaaa','#514d53',2),rect(0,400,672,80,'url(#road)','#272c3b',3),rect(0,466,672,14,'#565d6c','none',0)]
 for x in range(0,672,72):
  contents.append(line(x,375,x-2,396,'#a88b84',1))
 for x in [22,163,319,481,630]:
  contents.append(rect(x,440,51,5,'#f1e7cf','none',0,2))
 for j in range(140):
  x=rng.randint(0,672);y=rng.randint(400,480)
  contents.append(circle(x,y,rng.choice([0.6,0.7,1]),rng.choice(['#454b53','#81868d','#98908a']),'none',0))
 save(f'city_{layer}.png',672,480,''.join(contents))


# Character 1: lanky kid hero with huge swept hair, pointy nose and oversized eyes.
def boy(step=0,duck=False):
 body=''
 body+=ellipse(52,110,28,5,'#2d3140','none',0)
 if duck:
  body+=path('M28 73 Q43 67 59 69 L61 86 Q48 90 34 87 L27 81 Z','#fbfbf5')
  body+=path('M34 88 L28 101 M56 88 L64 101','none','#e0ae71',5)
  body+=path('M25 102 L37 102 M58 102 L69 102','none','#1d2231',6)
  body+=ellipse(44,45,16,29,'#e7bd82')
  body+=path('M58 50 Q78 43 82 29 Q84 17 73 17 Q62 6 46 9 Q27 7 18 18 Q12 28 18 40 Q28 36 36 33 Q50 31 58 50 Z','#141824')
  body+=path('M58 54 Q66 54 70 50','none','#d0915d',2)
  body+=path('M39 72 L22 81','none','#deb074',5)
  body+=path('M52 73 L69 80','none','#deb074',5)
 else:
  body+=path('M37 59 Q44 57 57 58 L60 82 Q48 86 36 83 Z','#fbfaf3')
  body+=path('M38 82 L30 104 M57 82 L66 104','none','#e0ae71',5)
  body+=path('M29 104 L39 104 M66 104 L76 104','none','#1d2231',6)
  arm_l='M36 65 L23 74' if step else 'M36 65 L20 67'
  arm_r='M58 65 L70 76' if step else 'M58 65 L73 66'
  body+=path(arm_l,'none','#deb074',5)
  body+=path(arm_r,'none','#deb074',5)
  body+=ellipse(46,37,16,31,'#e7bd82')
  body+=path('M58 44 Q78 38 84 22 Q85 9 73 8 Q63 -1 48 2 Q31 -2 20 8 Q13 18 16 31 Q31 27 42 24 Q53 22 58 44 Z','#141824')
  body+=path('M55 54 Q63 56 68 53','none','#d0915d',2)
 body+=ellipse(38,37,8,10,'#fffef5')+ellipse(52,38,9,10,'#fffef5')
 body+=circle(40,39,2.8,'#151822','none',0)+circle(54,40,2.8,'#151822','none',0)
 body+=path('M55 44 L66 47','none','#d0915d',2)
 body+=path('M55 44 Q62 46 65 43','none','#cc9966',1)
 return body
save('hero_boy.png',100,115,boy())
save('hero_boy_run.png',100,115,boy(step=1))
save('hero_boy_duck.png',100,115,boy(duck=True))

# Character 2: stretch-limbed green gecko with backward cap and baseball tee.
def gecko(step=0,duck=False):
 c=''
 c+=ellipse(52,111,31,5,'#2d3140','none',0)
 if duck:
  c+=path('M31 86 Q44 67 63 67 Q73 68 80 79 Q64 83 57 91 Q47 101 35 105','none','#5fe067',14)
  c+=path('M39 71 Q52 66 68 71 L68 85 Q54 89 43 86 Z','#f7f7f4')
  c+=path('M31 71 L40 71 Q43 76 43 86 L31 85 Z','#c8453e')
  c+=path('M67 71 L77 72 L77 85 L67 85 Z','#c8453e')
  head_y=39
 else:
  c+=path('M44 47 Q27 61 32 82 Q40 103 58 101 Q70 99 71 84 Q73 68 59 60','none','#59de67',12)
  c+=path('M37 63 Q52 59 69 63 L69 83 Q55 87 42 84 Z','#f7f7f4')
  c+=path('M29 64 L39 64 Q43 71 42 83 L30 83 Z','#c8453e')
  c+=path('M68 64 L79 64 L80 82 L69 83 Z','#c8453e')
  if step:
   c+=path('M43 82 L35 103','none','#56c56a',5)
   c+=path('M58 82 L72 103','none','#56c56a',5)
  else:
   c+=path('M45 82 L39 104','none','#56c56a',5)
   c+=path('M57 82 L63 104','none','#56c56a',5)
  c+=path('M43 68 L28 76','none','#56c56a',4)
  c+=path('M64 68 L78 75','none','#56c56a',4)
  head_y=31
 c+=path(f'M36 {head_y+12} Q41 {head_y-9} 57 {head_y-7} Q72 {head_y-5} 80 {head_y+8} Q67 {head_y+21} 49 {head_y+23} Q39 {head_y+23} 36 {head_y+12} Z','#79f283')
 c+=ellipse(48,head_y,10,12,'#fffef6')+ellipse(64,head_y+2,11,12,'#fffef6')
 c+=circle(50,head_y+1,3,'#20252f','none',0)+circle(66,head_y+3,3,'#20252f','none',0)
 c+=path(f'M53 {head_y+14} Q66 {head_y+18} 73 {head_y+12}','none','#256f63',2)
 c+=path(f'M34 {head_y-8} L35 {head_y-18} Q45 {head_y-29} 58 {head_y-28} Q71 {head_y-28} 80 {head_y-16} L87 {head_y-9} Q74 {head_y-3} 64 {head_y-5} Q51 {head_y-8} 34 {head_y-8} Z','#29508d')
 c+=path(f'M71 {head_y-13} Q84 {head_y-13} 92 {head_y-6} Q82 {head_y+1} 69 {head_y-1} Z','#2d5b9a')
 return c
save('hero_gecko.png',100,115,gecko())
save('hero_gecko_run.png',100,115,gecko(step=1))
save('hero_gecko_duck.png',100,115,gecko(duck=True))

# The antagonist: flamboyant cartoon driver in a mustard hot-rod with teal smoke.
car=''
car+=ellipse(65,88,63,9,'#394256','none',0)
car+=path('M13 45 Q19 25 42 23 L89 25 L113 50 L137 54 L143 79 L4 80 L4 55 Z','#dda34a')
car+=path('M46 27 L82 26 L104 51 L31 50 Z','#7ed5d5')
car+=path('M59 29 Q57 16 69 9 Q93 2 99 29 L85 42 Z','#e8b58c')
car+=path('M53 18 Q59 -2 76 4 Q87 -8 99 17 L97 25 Q75 15 53 26 Z','#211b2c')
car+=path('M59 28 L74 34 M85 30 L95 33','none','#242231',3)
car+=rect(10,57,128,23,'#e9b858','#35303a',3,8)
car+=circle(31,82,15,'#292630')+circle(31,82,6,'#b0cbd4','#222',2)
car+=circle(115,82,15,'#292630')+circle(115,82,6,'#b0cbd4','#222',2)
car+=rect(135,62,9,11,'#eb6662','#27252f',2,2)
save('villain_car.png',152,100,car)

# Props
cone=ellipse(26,51,25,6,'#202a38','none',0)+path('M26 5 L43 47 L10 47 Z','#ff9453')+path('M20 30 L32 30 L35 38 L17 38 Z','#fcf3cc','none',0)+rect(2,46,48,8,'#e76b43','#31333e',2,3)
save('cone.png',52,60,cone)
barrel=ellipse(25,70,24,6,'#333344','none',0)+rect(8,14,36,56,'#6c8bb4','#29283a',3,5)+rect(5,10,42,12,'#b4c7ce','#29283a',3,4)+rect(13,33,28,10,'#9ed2c9','none',0,2)
save('bin.png',52,76,barrel)
barrier=rect(0,16,72,16,'#f2d358','#3d3232',2,3)
for x in range(4,72,22):barrier+=path(f'M{x} 29 l12 -12 l8 0 l-12 12 Z','#dd7764','none',0)
barrier+=rect(7,31,7,35,'#46555f','#2e3039',2,1)+rect(59,31,7,35,'#46555f','#2e3039',2,1)
save('barrier.png',72,70,barrier)
coin=circle(20,20,17,'#ffd45c','#af702c',3)+circle(20,20,12,'none','#fff0a4',2)+path('M20 8 L23 17 L32 17 L25 22 L28 31 L20 25 L12 31 L15 22 L8 17 L17 17 Z','#fff4af','#d49a29',1)
save('coin.png',40,40,coin)
logo=circle(60,60,54,'#2fcce0','#263148',5)+circle(60,60,40,'#7fdb83','#263148',2)+path('M33 85 L42 27 L63 44 L79 22 L87 86 Z','#fbe0aa')+circle(47,53,5,'#263148','none',0)+circle(75,53,5,'#263148','none',0)
save('logo.png',120,120,logo)
