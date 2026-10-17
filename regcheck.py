import ssl,urllib.request as u,urllib.error,json
ctx=ssl._create_unverified_context()
def get(url,t=8):
    try:
        r=u.urlopen(u.Request(url,headers={'Accept':'application/json'}),context=ctx,timeout=t); return r.status,r.read(4000)
    except urllib.error.HTTPError as e: return e.code,e.read(500)
    except Exception as e: return -1,str(e).encode()
U='https://userapi.amer-1.aivencloud.net'
for s in ['PreflightTarget','PreflightConfig','Ownership','RestartPolicy','WorkerPoolRef','BuildConfig','EnvVar']:
    st,b=get(U+'/schemas/%s.json'%s)
    print('==',s,st); print('  ',b[:500])
