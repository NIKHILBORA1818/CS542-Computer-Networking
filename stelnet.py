import os
import subprocess
import os.path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        resp = None
        query_components = parse_qs(urlparse(self.path).query)
        cmd = query_components["cmd"]
        print(f'Running cmd at Server: {cmd[0]}')

        runcmd = f'{cmd[0]}'

        if "GET" not in runcmd:
            if 'cd' in runcmd:
                split = runcmd.split()
                os.chdir(split[1])
                resp = f'Changed directory to: {os.getcwd()}'
                self.send_response(200)
                self.end_headers()
                self.wfile.write(resp.encode('utf-8'))
                return

            if 'pwd' in runcmd:
                print(f'pwd is : {os.getcwd()}')
                #runcmd = f'cd' #for windows

            p = subprocess.Popen(f'{runcmd}', stdout=subprocess.PIPE, shell=True)
            out = p.communicate()
            resp = out[0]

            if 'echo' in runcmd:
                resp = b'A new file is created on Server.'
            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp)
            return

        if 'HTTP/1.1' in runcmd:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Localhost server does not supports HTTP 1.1')
            return
        if 'GET /folder1/test.html' in runcmd:
            path =  os.getcwd() + os.sep + 'folder1' + os.sep + 'test.html'
            if not os.path.isfile(path):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'File does not exists on the server.')
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Welcome to Localhost Server: Supports HTTP 1.0')

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()


