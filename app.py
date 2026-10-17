import http.server, socketserver, os, json, subprocess, urllib.parse, socket
def t(h,p,to=5):
    s=socket.socket(); s.settimeout(to)
    try: s.connect((h,p)); return 'OPEN'
    except Exception as e: return type(e).__name__
    finally:
        try: s.close()
        except: pass
def probe():
    import time
    r={'cloud':os.environ.get('AIVEN_CLOUD','?'),'host':socket.gethostname()}
    r['myip']=subprocess.run("hostname -I 2>/dev/null || cat /proc/net/fib_trie | grep -m1 10.",shell=True,capture_output=True,text=True).stdout.strip()[:60]
    r['falcon']={str(p):t('193.122.235.156',p,6) for p in (5432,22,80,443,8080,8443)}
    r['controls']={'api.aiven.io:443':t('api.aiven.io',443,5),'example.com:443':t('example.com',443,5)}
    return r
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path)
        body=json.dumps(probe() if u.path=='/probe' else {'ok':1}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",int(os.environ.get("PORT",3000))),H) as s: s.serve_forever()
