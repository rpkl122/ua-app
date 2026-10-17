import http.server, socketserver, os, json, urllib.parse, socket, threading, struct
HITS=[]
# serve a MySQL-protocol responder on 3000 too? only HTTP exposed. Instead: log hits + relay marker
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); HITS.append((self.client_address[0],u.path))
        body=json.dumps({'hits':HITS,'ip':subprocess.run('hostname -i',shell=True,capture_output=True,text=True).stdout.strip()}).encode() if u.path=='/hits' else json.dumps({'ok':1}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a):
        HITS.append(('log',a))
import subprocess
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",3000),H) as s: s.serve_forever()
