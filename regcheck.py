import paramiko,socket
# enumerate auth methods per username via paramiko transport
def methods(host,user,port=22,t=6):
    try:
        sock=socket.socket(); sock.settimeout(t); sock.connect((host,port))
        tr=paramiko.Transport(sock)
        tr.start_client(timeout=t)
        try:
            tr.auth_none(user)
        except paramiko.BadAuthenticationType as e:
            return list(e.allowed_types)
        except Exception as e:
            return f"{type(e).__name__}"
        finally:
            tr.close()
            sock.close()
        return "auth_none_ACCEPTED(!)"
    except Exception as e: return f"{type(e).__name__}:{str(e)[:50]}"
hosts=['10.150.0.3','10.150.0.4','10.150.0.5','10.150.0.7','10.150.0.8','10.150.0.15','10.150.0.25','10.150.0.50','10.150.0.200','10.150.0.254']
print('=== auth methods per user ===')
for h in hosts:
    for u in ['root','aiven','admin','postgres','ubuntu','builder']:
        m=methods(h,u)
        if 'publickey' in str(m) or 'password' in str(m) or 'ACCEPTED' in str(m):
            print(f"{h} user={u} -> {m}")
print('DONE-METHODS')
print('=== key algorithms offered (server host keys / kex) ===')
for h in ['10.150.0.3','10.150.0.254']:
    try:
        sock=socket.socket(); sock.settimeout(6); sock.connect((h,22))
        tr=paramiko.Transport(sock); tr.start_client(timeout=6)
        print(h,'remote_version:',tr.remote_version)
        print(h,'server_key:',tr.get_security_options().key_types[:5])
        tr.close()
    except Exception as e: print(h,'ERR',type(e).__name__,str(e)[:60])
