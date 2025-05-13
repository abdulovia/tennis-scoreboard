from http.server import HTTPServer
from custom_handler import CustomHTTPRequestHandler


def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler):
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
