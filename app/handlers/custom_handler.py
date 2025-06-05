from http.server import BaseHTTPRequestHandler

import urllib

from app.router.router import Router


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    router = Router()

    def do_GET(self):
        urlparsed = urllib.parse.urlparse(self.path)
        controller = self.router.get_controller_method(self.command, urlparsed.path)
        response = controller(urlparsed.query)
        self.respond(response)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        urlparsed = urllib.parse.urlparse(self.path)
        controller = self.router.get_controller_method(self.command, urlparsed.path)
        response = controller(urlparsed.query, post_data.decode())
        self.respond(response)

    def respond(self, response):
        self.send_response(response.code, response.message)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response.to_str().encode())
