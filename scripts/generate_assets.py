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

# Character 1: small brave adventurer with jet-black swoosh and cream face, original design.
def boy(step=0,duck=False):
 if duck:
  content=ellipse(49,99,31,6,'#252b39','none',0)
  content+=path('M27 65 L64 64 L74 77 L47 87 L27 77 Z','#fffaf1')
  content+=path('M42 81 L29 100 M62 82 L71 97','none','#292631',5)
  content+=ellipse(42,40,20,31,'#f1c681')
  content+=path('M21 25 Q14 0 40 4 Q60 -4 70 22 L63 34 Q43 18 20 34 Z','#171b28')
 else:
  content=ellipse(49,108,27,5,'#252b39','none',0)
  content+=path('M37 69 L40 91 L28 106 M54 69 L59 89 L70 106','none','#e5af72',6)
  content+=path('M26 107 L39 108 M62 108 L78 110','none','#1e2230',7)
  content+=path('M34 48 L64 51 L62 80 L31 77 Z','#f8faf2')
  content+=path('M32 58 L17 76 L10 68 M62 57 L75 67 L83 62','none','#e5af72',6)
  if step:
   content+=path('M38 79 L26 105 M57 79 L71 104','none','#352a31',4)
  content+=ellipse(43,33,21,29,'#f0c884')
  content+=path('M20 28 Q9 6 36 6 Q50 -3 63 11 L63 27 Q54 17 48 20 Q34 15 22 37 Z','#151723')
  content+=path('M20 21 Q18 2 32 1 Q56 -4 59 8','none','#101724',5)
 content+=ellipse(38,36,7,9,'#fffefa')+ellipse(54,37,8,9,'#fffefa')
 content+=circle(40,39,2.5,'#171723','none',0)+circle(54,40,2.5,'#171723','none',0)
 content+=path('M46 45 Q54 48 59 44','none','#9e5153',2)
 return content
save('hero_boy.png',100,115,boy())
save('hero_boy_run.png',100,115,boy(step=1))
save('hero_boy_duck.png',100,115,boy(duck=True))

# Character 2: smiling jade-green lizard with backwards sailor-blue cap.
def gecko(step=0,duck=False):
 c=ellipse(49,109,33,5,'#30323d','none',0)
 if duck:
  c+=path('M20 83 Q43 68 67 82 Q77 95 63 99 Q49 92 33 103','none','#4fd76d',16)
  cy=54
 else:
  c+=path('M42 49 Q20 62 38 87 Q58 107 70 90 Q80 75 61 66','none','#4bd868',12)
  c+=path('M53 70 L75 91 L82 107 M41 70 L26 92 L21 105','none','#58cb6c',6)
  c+=path('M38 55 L23 68 M60 53 L74 68','none','#4bc968',5)
  cy=33
 c+=path(f'M30 {cy+18} Q36 {cy-16} 64 {cy-4} L76 {cy+13} Q55 {cy+17} 44 {cy+29} Z','#74e98b')
 c+=ellipse(45,cy,14,16,'#fff8ee')+ellipse(65,cy+2,12,15,'#fff8ee')
 c+=circle(48,cy+1,4,'#222837','none',0)+circle(67,cy+3,4,'#222837','none',0)
 c+=path(f'M49 {cy+23} Q62 {cy+29} 76 {cy+19}','none','#1b7867',3)
 c+=path(f'M30 {cy-9} L30 {cy-19} Q47 {cy-36} 72 {cy-17} L83 {cy-7} Z','#284a81')
 c+=path(f'M65 {cy-12} Q84 {cy-13} 92 {cy-3} Q76 {cy+2} 64 {cy-2} Z','#2e5c92')
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
