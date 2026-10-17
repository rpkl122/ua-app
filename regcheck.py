import ssl,urllib.request as u,urllib.error,json
ctx=ssl._create_unverified_context()
def get(url,t=6):
    try:
        r=u.urlopen(url,context=ctx,timeout=t); return r.status,r.read(6000)
    except urllib.error.HTTPError as e: return e.code,e.read(600)
    except Exception as e: return -1,str(e).encode()
U='https://userapi.amer-1.aivencloud.net'
st,b=get(U+'/schemas/Service.json')
print('Service.json status',st)
try:
    d=json.loads(b); print('props:',list(d.get('properties',{}).keys()))
    print(json.dumps(d,indent=1)[:4000])
except Exception as e: print('raw',b[:2000])
# try to enumerate other schemas by wordlist
print('=== schema name discovery ===')
for n in ['BuildLogs','BuildResult','Deploy','Environment','EnvVar','Port','Source','Auth','Token','Credential','Webhook','Domain','Certificate','Route','Ingress','Health','Usage','Quota','Secret']:
    st2,b2=get(U+'/schemas/%s.json'%n)
    if st2==200 and b2!=b'null': print('SCHEMA',n,'->',b2[:200])
print('DONE')
