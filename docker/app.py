import http.server, socketserver, os, datetime
PORT = 8000
class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b"ok\n"
        else:
            body = (f"docker-lab v1.0\nhost={os.uname().nodename}\ntime={datetime.datetime.now():%F %T}\n").encode()
        self.send_response(200); self.send_header("Content-Type","text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), H) as s: s.serve_forever()
