import socket
import threading
import typing as tp

from .handlers import BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        self.backlog_size = backlog_size
        self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout = timeout
        self._threads: tp.List[threading.Thread] = []

    def serve_forever(self) -> None:
        address = (self.host, self.port)
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        serv_socket.bind(address)
        serv_socket.listen(self.backlog_size)
        print(f"Listening on http://{address[0]}:{address[1]}/")

        for thread in range(self.max_workers):
            self._threads.append(threading.Thread(target=self.handle_accept, args=(serv_socket,)))
            self._threads[thread].start()
        try:
            for i in self._threads:
                i.join()
        except KeyboardInterrupt:
            print("Good bye...")
            serv_socket.close()

    def handle_accept(self, server_socket: socket.socket) -> None:
        while True:
            client_socket, address = server_socket.accept()
            client_socket.settimeout(self.timeout)
            request = self.request_handler_cls(client_socket, address, server_socket)
            print(f"Hello http://{address[0]}:{address[1]}/")
            request.handle()


class HTTPServer(TCPServer):
    pass

if __name__ == "__main__":
    server = TCPServer(host="localhost", port=5050)
    server.serve_forever()