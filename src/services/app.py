from http.server import HTTPServer
from src.services.http_handler import HttpHandler
from src.utils.enviroment import EnvironmentVariables


class App:
    def __init__(self, server=HTTPServer, handler=HttpHandler) -> None:
        self.server = server
        self.handler = handler

    def run(self) -> None:
        env = EnvironmentVariables()
        server_address = ("", int(env.get("app", "PORT")))
        http = self.server(server_address, self.handler)
        try:
            http.serve_forever()
        except KeyboardInterrupt:
            http.server_close()
