from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from jinja2 import Environment, FileSystemLoader
import mimetypes
import pathlib
import urllib.parse
from src.utils.storage import Storage
from datetime import datetime


class HttpHandler(BaseHTTPRequestHandler):

    TEMPLATES_DIR = pathlib.Path(__file__).parent.parent.joinpath("templates")
    STATIC_DIR = pathlib.Path(__file__).parent.parent.joinpath("static")

    def __init__(self, request, client_address, server):
        self.storage = Storage()
        super().__init__(request, client_address, server)

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html("index.html")
        elif pr_url.path == "/message":
            self.send_html("message.html")
        elif pr_url.path == "/read":
            self.send_messages_list()
        else:
            filename = self.STATIC_DIR.joinpath(self.path[1:])
            if filename.exists():
                self.send_static(filename)
            else:
                self.send_html("error.html", HTTPStatus.NOT_FOUND)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }

        storage_data = self.storage.load_data()

        if not storage_data:
            storage_data = {}

        storage_data[str(datetime.now())] = data_dict
        self.storage.save_data(storage_data)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_html(self, filename, status=HTTPStatus.OK):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(self.TEMPLATES_DIR.joinpath(filename), "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename, status=HTTPStatus.OK):
        mt = mimetypes.guess_type(self.path)
        self.send_response(status)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def send_messages_list(self, status=HTTPStatus.OK):
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIR))
        template = env.get_template("messages_list.html")
        messages = self.storage.load_data()
        output = template.render(
            messages=messages,
        )
        if not output:
            output = {}
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(output.encode())
