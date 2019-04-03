import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import ssl
import json
import urllib3

username = ""
stop_threads = False


class S(BaseHTTPRequestHandler):
    BaseHTTPRequestHandler.sys_version = ""
    BaseHTTPRequestHandler.server_version = "nginx"

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '3600')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT, DELETE, HEAD')
        self.send_header('Expires', 'Mon, 1 Aug 2011 09:00:00 GMT')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        self.send_header('Connection', 'close')
        self.end_headers()

    def do_GET(self):
        self.forward_request('GET')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = json.dumps(json.loads(data_string))

        self.forward_request('POST', data)

    def forward_request(self, method, data=""):
        global username

        url = 'http://192.168.178.178{}'.format(self.path)
        forward = urllib3.PoolManager()

        if method == 'POST':
            flush = threading.Thread(target=http_flush)
            flush.start()

            data_new = "{'success': {'username': 'UtIMCRQDSP00Vf0QpEKcLlXCksq9uCTw8kaDjM1T'}}"
        else:
            req = forward.request(method, url, body=data.encode())
            data_new = json.loads(req.data)
            data_new['apiversion'] = '1.0.0'
            data_new['mac'] = 'e4:b3:18:8a:fa:7f'
            data_new['bridgeid'] = 'E4B3188AFA7FAFAB'

        self._set_headers()
        self.wfile.write(json.dumps(data_new).encode())


def run_https(server_class=HTTPServer, handler_class=S, port=443):
    global stop_threads

    httpsd = server_class(('', port), handler_class)
    httpsd.socket = ssl.wrap_socket(httpsd.socket, certfile='./server.pem', server_side=True)

    print('Starting https server')

    while not stop_threads:
        httpsd.handle_request()

    print("Closed https server")


def run_http(server_class=HTTPServer, handler_class=S, port=80):
    global stop_threads

    httpd = server_class(('', port), handler_class)

    print("Starting http server")

    while not stop_threads:
        httpd.handle_request()

    print("Closed http server")


def http_flush():
    ip = "http://192.168.178.178/api/"
    global username
    step = 0

    while True:
        new_user = requests.post(ip, data="{\"devicetype\": \"openhabHueBinding#openhab\"}")
        response = json.loads(new_user.content)[0]
        step += 1

        if 'success' in response:
            username = response['success']['username']
            print("Made a connection, after " + str(step) + " packages send.                          ")
            break
        else:
            print("Link button has not been pressed, " + str(step) + " packages send.", end="\r")

        time.sleep(1)