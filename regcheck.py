import socket
def ssh_methods(h,p=22):
    try:
        s=socket.socket(); s.settimeout(4); s.connect((h,p))
        b=s.recv(120); s.sendall(b'SSH-2.0-Probe\r\n')
        import time; time.sleep(0.5)
        d=s.recv(2048); s.close()
        # parse KEXINIT for server host key algos + auth methods come after auth, so just report kex
        return b.decode('utf-8','replace').strip()
    except Exception as e: return f"ERR {type(e).__name__}"
for h in ['10.150.0.3','10.150.0.4','10.150.0.5','10.150.0.7','10.150.0.50','10.150.0.200','10.150.0.254']:
    print(h, ssh_methods(h))
# is there a route to other subnets or the falcon internal ip?
print('=== routes / other subnets ===')
try: print(open('/proc/net/route').read())
except Exception as e: print('route',e)
# dns
print('=== resolv ==='); print(open('/etc/resolv.conf').read())
# try resolving internal names
for n in ['10.150.0.3','host-10-150-0-3','ip-10-150-0-3']:
    print(n)
import socket
for name in ['falcon-bug-bounty-flag-pgsql-dev-sandbox','falcon-bug-bounty-flag-pgsql-dev-sandbox.aiven.local']:
    try: print(name,socket.gethostbyname_ex(name))
    except Exception as e: print(name,'NO')
