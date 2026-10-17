import os,glob,re
pats=re.compile(rb'(NOMAD_TOKEN|VAULT_TOKEN|CONSUL_HTTP_TOKEN|secret_id|client_token|X-Nomad-Token|nomad_token)',re.I)
found=[]
# env of every readable proc
for pid in os.listdir('/proc'):
    if not pid.isdigit(): continue
    try:
        e=open('/proc/%s/environ'%pid,'rb').read()
        if pats.search(e):
            found.append(('ENV pid%s'%pid, e[:400]))
    except Exception: pass
# files
for root in ['/alloc','/local','/secrets','/run','/etc','/var/run','/opt','/srv']:
    for dp,dn,fn in os.walk(root):
        if any(x in dp for x in ('site-packages','node_modules','/proc')): continue
        for f in fn:
            p=os.path.join(dp,f)
            try:
                if os.path.getsize(p)>200000: continue
                d=open(p,'rb').read()
                if pats.search(d): found.append(('FILE '+p, d[:300]))
            except Exception: pass
print("FOUND %d"%len(found))
for k,v in found[:30]: print(k,'::',v[:150])
