import socket
def t(h,p,t=0.6):
    try:
        s=socket.socket(); s.settimeout(t); s.connect((h,p)); s.close(); return True
    except Exception: return False
# focused: the hosts we saw with :22, plus a quick sweep of the /24 on just a few ports
hosts=['10.150.0.1','10.150.0.2','10.150.0.3','10.150.0.4','10.150.0.5','10.150.0.6','10.150.0.7','10.150.0.50','10.150.0.200','10.150.0.254']
ports=[22,80,443,4646,8500,8200,5432,6379,9090,2375,3000,8080,10250,6443,2181,9200]
res={}
for h in hosts:
    o=[p for p in ports if t(h,p)]
    if o: res[h]=o
print('HOSTS:',res)
# banner grab on ssh of the ones that answered
for h in ['10.150.0.3','10.150.0.4','10.150.0.5','10.150.0.50','10.150.0.200','10.150.0.254','10.150.0.1','10.150.0.2']:
    try:
        s=socket.socket(); s.settimeout(3); s.connect((h,22)); d=s.recv(120); s.close()
        print(h,'SSH:',d.decode('utf-8','replace').strip())
    except Exception as e:
        pass
print('DONE')
