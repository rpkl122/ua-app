import http.server, socketserver, json, urllib.parse
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try: log=open('/tmp/rogue.log').read()
        except Exception: log=''
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(json.dumps({"log":log}).encode())
    def log_message(self,*a): pass
import threading
threading.Thread(target=lambda: socketserver.TCPServer(("0.0.0.0",3000),H).serve_forever(),daemon=True).start()
import rogue_mysql
