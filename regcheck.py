import socket
hosts=['10.150.0.1','10.150.0.2','10.150.0.3','10.150.0.4','10.150.0.5','10.150.0.6','10.150.0.7','10.150.0.8','10.150.0.10','10.150.0.15','10.150.0.20','10.150.0.25','10.150.0.50','10.150.0.100','10.150.0.200','10.150.0.254']
ports=[22,80,443,4646,4647,8500,8600,8200,8443,9001,5432,6379,26257,8080,9090,2379,2380,10250,6443,9200,5601,2181,9092,19335,9702,2376,11000,11001,11002]
def t(h,p,t=0.5):
    try:
        s=socket.socket(); s.settimeout(t); s.connect((h,p)); s.close(); return True
    except Exception: return False
res={}
for h in hosts:
    o=[p for p in ports if t(h,p)]
    if o: res[h]=o
print('SCAN:',res)
# http probe responsive web ports
import ssl,urllib.request as u
for h,ps in res.items():
    for p in ps:
        if p in (80,8080,9001,9090,8443,4646):
            for scheme in (['http'] if p!=8443 else ['https']):
                try:
                    url=f"{scheme}://{h}:{p}/"
                    ctx=ssl._create_unverified_context()
                    r=u.urlopen(url,context=ctx,timeout=4); print(h,p,scheme,'->',r.status,r.read(120)[:100])
                except Exception as e: print(h,p,scheme,'ERR',type(e).__name__)
print('DONE')
