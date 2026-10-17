import ssl,urllib.request as u,urllib.error,json
ctx=ssl._create_unverified_context()
def get(url,t=8):
    try:
        r=u.urlopen(url,context=ctx,timeout=t); return r.status,r.read(20000)
    except urllib.error.HTTPError as e: return e.code,e.read(600)
    except Exception as e: return -1,str(e).encode()
U='https://userapi.amer-1.aivencloud.net'
for spec in ['/openapi.json','/openapi.yaml','/docs','/swagger.json','/api/openapi.json','/v1/openapi.json','/schemas/Ownership.json','/schemas/WorkerPoolRef.json','/schemas/PreflightConfig.json','/schemas/ServicePort.json']:
    st,b=get(U+spec)
    print('==',spec,'->',st,len(b))
    if st==200 and spec=='/openapi.json':
        try:
            d=json.loads(b)
            print('  title:',d.get('info',{}).get('title'),'ver:',d.get('info',{}).get('version'))
            for path,methods in d.get('paths',{}).items():
                print('   ROUTE:',path,list(methods.keys()))
        except Exception as e: print('  parse',e, b[:300])
    elif st==200:
        print('  ',b[:400])
