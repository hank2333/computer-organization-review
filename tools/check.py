from pathlib import Path
from urllib.parse import unquote,urlsplit
from html.parser import HTMLParser
import runpy,json,random

ROOT=Path(__file__).resolve().parent.parent
data=runpy.run_path(str(ROOT/'tools/build.py'))
class Parse(HTMLParser):
 def __init__(self): super().__init__(); self.ids=[]; self.links=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='a' and 'href' in a:self.links.append(a['href'])

docs={}
for name in ('index.html',data['KN'],data['EX']):
 parser=Parse(); txt=(ROOT/name).read_text(encoding='utf-8'); parser.feed(txt)
 assert len(parser.ids)==len(set(parser.ids)),f'duplicate ids {name}'
 assert '�' not in txt and '????' not in txt and '\x00' not in txt
 docs[name]=parser
for name,doc in docs.items():
 for href in doc.links:
  u=urlsplit(href)
  if u.scheme: continue
  dest=unquote(u.path) or name
  assert (ROOT/dest).exists(),(name,href)
  if u.fragment and dest.endswith('.html'):
   assert unquote(u.fragment) in docs[dest].ids,(name,href)
assert len(data['quizzes'])==36
assert data['flags'](0x7f,1)==['80H',0,1,1,1,0,0]
assert data['flags'](0xf8,0x7f,8,True)==['79H',0,1,0,1,0,0]
# Independent decimal check against all valid pairs of packed BCD digits.
for a in range(100):
 for b in range(100):
  v=data['daa']((a//10)*16+a%10,(b//10)*16+b%10)
  out=int(v[3][:-1],16)
  assert (out>>4)*10+(out&15)+100*v[4]==a+b
# Validate arithmetic flag formulas against signed integer range, exhaustively for bytes.
for a in range(256):
 for b in range(256):
  sa=a-256 if a>127 else a;sb=b-256 if b>127 else b
  for sub in (False,True):
   f=data['flags'](a,b,8,sub); exact=sa-sb if sub else sa+sb
   assert f[2]==int(not -128<=exact<=127)
   assert f[4]==int((a&15)<(b&15)) if sub else f[4]==int((a&15)+(b&15)>15)
# Model E39 register-level arithmetic and its division guard, including edge cases.
def s16(v): return (v&65535)-65536 if (v&32768) else v&65535
def split(v): return ((v>>16)&65535,v&65535)
def join(h,l): return ((h<<16)|l)-4294967296 if h&32768 else (h<<16)|l
def addpair(h,l,h2,l2):
 t=l+l2;return (h+h2+(t>>16))&65535,t&65535
def subpair(h,l,h2,l2):return (h-h2-int(l<l2))&65535,(l-l2)&65535
def simulate(x,y,z,v):
 h,l=split(x*y); zh,zl=split(z);h,l=addpair(h,l,zh,zl);h,l=subpair(h,l,0,540)
 vh,vl=split(v);h,l=subpair(vh,vl,h,l);n=join(h,l)
 expected=v-(x*y+z-540); assert n==expected
 if x==0:return
 # The NEG low / ADC high,0 / NEG high sequence computes unsigned magnitude.
 if h&32768:
  low=(-l)&65535; high=(-(h+int(l!=0)))&65535
 else: high,low=h,l
 assert (high<<16|low)==abs(n)
 divisor=(-x if x<0 else x)&65535
 limit=divisor*(32769 if (h^(x&65535))&32768 else 32768)
 safe=(high<<16|low)<limit
 q=abs(n)//abs(x);q=-q if (n<0)^(x<0) else q
 assert safe==(-32768<=q<=32767)
rng=random.Random(20261122)
values=[-32768,-32767,-1,0,1,32766,32767]
for x in values:
 for y in values:
  for z in values:
   for v in values: simulate(x,y,z,v)
for _ in range(10000):simulate(*(rng.randint(-32768,32767) for _ in range(4)))


print("PASS: HTML links, IDs, quiz data, exhaustive BCD/flag checks, arithmetic boundary checks")
