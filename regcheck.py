import socket
def banner(h,p,t=3):
    try:
        s=socket.socket(); s.settimeout(t); s.connect((h,p))
        try: d=s.recv(200)
        except Exception: d=b''
        s.close(); return d.decode('utf-8','replace').strip()[:150]
    except Exception as e: return f"ERR {type(e).__name__}"
print('=== SSH banners (internal 10.150.0.x) ===')
for i in [1,2,3,4,5,10,20,50,100,150,200,254]:
    h='10.150.0.%d'%i
    # ssh banner
    b=banner(h,22,3)
    if not b.startswith('ERR'): print(h,'22:',b)
print('=== full /24 sweep top ports ===')
def t(h,p,t=0.4):
    try:
        s=socket.socket(); s.settimeout(t); s.connect((h,p)); s.close(); return True
    except Exception: return False
found={}
for i in range(1,255):
    h='10.150.0.%d'%i
    for p in [22,80,443,4646,8500,8200,5432,6379,9090,2375,2376,3000,8080,8443,10250,10255,6443,2181,9092,9200,9100]:
        if t(h,p):
            found.setdefault(h,[]).append(p)
print('ALIVE HOSTS:',found)
