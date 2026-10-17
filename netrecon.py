import socket,ipaddress,concurrent.futures as cf
def t(ip,p,to=1.0):
    try:
        s=socket.socket(); s.settimeout(to); s.connect((str(ip),p)); s.close(); return True
    except Exception: return False
LABEL=''
print("=== internal subnet scan (app pod netns) ===")
results={}
def chk(args):
    ip,p=args
    if t(ip,p): return (str(ip),p)
    return None
targets=[]
for net in ['10.150.0.0/24','10.0.0.0/24','10.1.0.0/24','10.1.8.0/24','172.16.0.0/24','172.17.0.0/24','192.168.0.0/24','10.128.0.0/24','10.100.0.0/24']:
    try:
        for ip in list(ipaddress.ip_network(net).hosts())[:60]:
            for p in [5432,22,80,443,8500,8200,4646,2375]:
                targets.append((ip,p))
    except Exception: pass
print("targets:",len(targets))
with cf.ThreadPoolExecutor(max_workers=300) as ex:
    for r in ex.map(chk,targets):
        if r: results.setdefault(r[0],[]).append(r[1])
for k in sorted(results): print("ALIVE",k,results[k])
print("=== falcon full-ish port scan ===")
falcon='193.122.235.156'
openp=[]
for p in list(range(1,2000))+[2375,2376,4646,5432,5433,5434,6379,8080,8443,9000,9090,9200,10250,19335,9702,6432,8443,3100,3000,5000,8000]:
    if t(falcon,p,0.6): openp.append(p)
print("falcon open:",openp if openp else "ALL FILTERED")
print("=== falcon internal ips ===")
for ip in ['10.1.8.115','10.1.8.114','10.1.8.116','10.1.8.1','10.1.0.1']:
    o=[p for p in [5432,22,80,443] if t(ip,p,0.8)]
    if o: print("INT-ALIVE",ip,o)
print("done")
