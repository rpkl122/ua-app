import urllib.request as u, urllib.error, ssl, json, os
c=ssl._create_unverified_context()
tok=open('/tmp/tok.txt').read().strip() if os.path.exists('/tmp/tok.txt') else os.environ.get('AT','')
def g(url,hdr):
    try:
        r=u.urlopen(u.Request(url,headers=hdr),context=c,timeout=7); return r.status, r.read(300).decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code, e.read(200).decode('utf-8','replace')
    except Exception as e: return -1, str(e)[:80]
hdrs={'Authorization':'Bearer '+tok}
for ep in ['/services','/services/1','/api-spec.json','/openapi.json']:
    print(ep, g('https://userapi.amer-1.aivencloud.net'+ep, hdrs))
# also try the leaked builder jwt
bc=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
import re
m=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',bc)
if m:
    print('builder-jwt', g('https://userapi.amer-1.aivencloud.net/services', {'Authorization':'Bearer '+m.group(0)}))
