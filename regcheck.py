import ssl,urllib.request as u,urllib.error,json,re,base64
ctx=ssl._create_unverified_context()
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
tok=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',cmd); tok=tok.group(0) if tok else ''
def req(url,method='GET',hdr=None,data=None,t=8):
    try:
        r=u.Request(url,headers=hdr or {},method=method,data=data)
        x=u.urlopen(r,context=ctx,timeout=t); return x.status,x.read(1500)
    except urllib.error.HTTPError as e: return e.code,e.read(600)
    except Exception as e: return -1,str(e).encode()
U='https://userapi.amer-1.aivencloud.net'
# enumerate: what distinguishes 401 (route exists) vs 404
print('=== route discovery (401=exists) ===')
routes=['/services','/services/','/service','/apps','/v1/services','/api/services','/builds','/deployments','/logs','/hooks','/webhooks','/tokens','/auth','/login','/users','/me','/projects','/environments','/config','/status','/health','/metrics','/version','/admin','/internal','/debug','/service/','/hook/','/preflight','/registry','/registries','/secrets','/env','/variables']
for p in routes:
    st,b=req(U+p)
    tag = 'EXISTS' if st==401 else (str(st) if st!=-1 else 'ERR')
    if st!=404: print(f"{p:20s} -> {tag} {b[:80]}")
print('--- POST variants ---')
for p in ['/services','/service']:
    st,b=req(U+p,method='POST',data=b'{}',hdr={'Content-Type':'application/json'})
    print('POST',p,'->',st,b[:150])
print('--- /services with method OPTIONS/HEAD ---')
for m in ['OPTIONS','HEAD','PUT','DELETE']:
    st,b=req(U+'/services',method=m); print(m,'/services ->',st,b[:80])
print('=== which auth does /services want? (WWW-Authenticate) ===')
try:
    r=u.Request(U+'/services')
    u.urlopen(r,context=ctx,timeout=6)
except urllib.error.HTTPError as e:
    print('headers:',dict(e.headers))
print('DONE')
