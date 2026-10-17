import http.server, socketserver, json, sys
HITS=[]
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self): self.reply()
    def do_POST(self): self.reply()
    def do_PUT(self): self.reply()
    def reply(self):
        ln=int(self.headers.get('Content-Length',0) or 0); body=self.rfile.read(ln) if ln else b''
        HITS.append({'m':self.command,'p':self.path,'h':dict(self.headers),'b':body[:2000].decode('utf-8','replace')})
        open('/tmp/hits.json','w').write(json.dumps(HITS,indent=1))
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
class T(socketserver.ThreadingMixIn, socketserver.TCPServer): pass
T(("0.0.0.0",3000),H).serve_forever()
