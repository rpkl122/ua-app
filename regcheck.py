import ssl,urllib.request as u,urllib.error,json
ctx=ssl._create_unverified_context()
def raw(url,t=8):
    try:
        r=u.urlopen(u.Request(url,headers={'Accept':'application/json'}),context=ctx,timeout=t); return r.status,r.read(40000)
    except urllib.error.HTTPError as e: return e.code,e.read(800)
    except Exception as e: return -1,str(e).encode()
U='https://userapi.amer-1.aivencloud.net'
st,b=raw(U+'/api-spec.json')
print('api-spec.json ->',st,len(b))
if st==200:
    open('/app/api_spec.json','wb').write(b)
    try:
        d=json.loads(b)
        print('info:',d.get('info'))
        for path,methods in d.get('paths',{}).items():
            for m,info in methods.items():
                print('ROUTE',m.upper(),path, '::', info.get('summary','')[:80])
    except Exception as e: print('parse err',e,b[:500])
else:
    print('body:',b[:400])
    for alt in ['/api-spec.json','/openapi.json','/docs','/swagger.json']:
        st2,b2=raw(U+alt); print(alt,st2,len(b2))
