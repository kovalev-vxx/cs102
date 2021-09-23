import socket
import threading
import typing as tp

#from .handlers import BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        #request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        # @see: https://stackoverflow.com/questions/36594400/what-is-backlog-in-tcp-connections
        self.backlog_size = backlog_size
        #self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout = timeout
        self._threads: tp.List[threading.Thread] = []

    def serve_forever(self) -> None:
        # @see: http://veithen.io/2014/01/01/how-tcp-backlog-works-in-linux.html
        # @see: https://en.wikipedia.org/wiki/Thundering_herd_problem
        # @see: https://stackoverflow.com/questions/17630416/calling-accept-from-multiple-threads
        address = (self.host, self.port)
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        serv_socket.bind(address)
        serv_socket.listen(self.backlog_size)

        print(f"Listening on http://{address[0]}:{address[1]}/")

        try:
            while True:
                client_sock, client_addr = serv_socket.accept()
                print(f"client: {client_sock}, addr: {client_addr}")

                while True:
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    client_sock.sendall(data)
                client_sock.close()
        except KeyboardInterrupt:
            print("Good bye...")

    def handle_accept(self, server_socket: socket.socket) -> None:
        pass


class HTTPServer(TCPServer):
    pass

if __name__ == "__main__":
    server = TCPServer(host="localhost", port=5050)
    server.serve_forever()
