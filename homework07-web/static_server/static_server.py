import mimetypes
import pathlib
from datetime import datetime
import typing as tp
from urllib.parse import urlparse

from httpserver import BaseHTTPRequestHandler, HTTPRequest, HTTPResponse, HTTPServer
from url_normalize import url_normalize


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        url = urlparse(url_normalize(request.url.decode()))
        default_url = url.path

        if "%20" in default_url:
            default_url = default_url.replace("%20", " ")

        if url.path == ("/"):
            default_url = "/index.html"
        path = pathlib.Path(str(server.document_root.absolute()) + default_url)
        now = datetime.now()
        headers = {
            "Server": "GServer",
            "Date": now.strftime("%m/%d/%Y, %H:%M:%S"),
            "Content-Length": "0",
            "Content-Type": "None",
            "Allow": "GET, HEAD",
        }
        if request.method == b"GET" or request.method == b"HEAD":
            if path.exists() and path.is_file():
                body = b""
                if request.method == b"GET":
                    with open(path, "rb") as file:
                        body = file.read()
                headers["Content-Type"] = str(mimetypes.guess_type(path)[0])
                headers["Content-Length"] = str(len(body))
                return self.response_klass(status=200, headers=headers, body=body)
            return self.response_klass(status=404, headers=headers, body=b"")
        return self.response_klass(status=405, headers=headers, body=b"")


class StaticServer(HTTPServer):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = 5,
        request_handler_cls: tp.Type[StaticHTTPRequestHandler] = StaticHTTPRequestHandler,
        document_root: pathlib.Path = pathlib.Path("."),
    ) -> None:
        super().__init__(
            host=host,
            port=port,
            backlog_size=backlog_size,
            max_workers=max_workers,
            timeout=timeout,
            request_handler_cls=request_handler_cls,
        )
        self.document_root = document_root


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=60,
        document_root=document_root,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
