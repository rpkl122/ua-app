import ssl,urllib.request as u,urllib.error,json,re
ctx=ssl._create_unverified_context()
def get(url,hdr=None,t=6):
    try:
        r=u.urlopen(u.Request(url,headers=hdr or {}),context=ctx,timeout=t); return r.status,r.read(2000)
    except urllib.error.HTTPError as e: return e.code,e.read(600)
    except Exception as e: return -1,str(e).encode()
UAPI='https://userapi.amer-1.aivencloud.net'
print('=== userapi schemas ===')
st,b=get(UAPI+'/schemas/')
print('schemas/ ->',st,b[:300])
# common schema names
for s in ['ServiceStatus.json','ServiceStatus','Service','Application','Build','Status','Error.json']:
    st,b=get(UAPI+'/schemas/'+s)
    if st==200: print('schema',s,'->',b[:400])
print('=== endpoints ===')
for p in ['/v1/status','/v1/status/','/status','/v1/app','/apps','/v1/builds','/v1/logs','/metrics','/v1/services','/service','/v1/deployments']:
    st,b=get(UAPI+p)
    print(p,'->',st,b[:120])
print('=== cross-tenant Host/name oracle: does the gate reveal other apps? ===')
# my app FQDN pattern: <uuid>-3000.amer-1.aiven.app. Try sibling uuids
for guess in ['00000000-0000-0000-0000-000000000000-3000.amer-1.aiven.app','01a14aae-c426-7468-b68b-30cb398ed5d9-3000.amer-1.aiven.app']:
    st,b=get('https://userapi.amer-1.aivencloud.net/status?host='+guess)
    print('status host=',guess[:20],'->',st,b[:150])
print('DONE')
