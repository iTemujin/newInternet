import socket
import selectors
import types
import json

import time

sel = selectors.DefaultSelector()


class Server():
    def __init__(self, posta, identity_posta):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = 8080
        lsock.bind(('', PORT))
        lsock.listen()

        self.posta = posta

        self.local_ip = lsock.getsockname()
        self.posta.put(f'{self.local_ip[0]}:{self.local_ip[1]}')

        self.identity = identity_posta.get()

        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

    def _run_tagHere(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('', 5005))

        while True:
            data, addr = sock.recvfrom(1024)
            if data == b"DISCOVER_SERVER":
                # Válaszolunk, hogy itt vagyunk
                sock.sendto(b"SERVER_HERE", addr)

    def run(self):
        print(f'[{self.identity.get_family()}] Server...')
        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print(f'Accepted connection from {addr}')
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'', recv_buf=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(4096)

            if recv_data:
                data.recv_buf += recv_data
                while b'\n' in data.recv_buf:
                    line, data.recv_buf = data.recv_buf.split(b'\n', 1)
                    try:
                        message = json.loads(line.decode("utf-8"))
                        req = message.get('request')
                        if req == 'can i join':
                            response = json.dumps({'request': 'yes', 'clubName': 'Obj2'}).encode('utf-8') + b'\n'
                            data.outb += response
                        elif req == 'get_club':
                            response = json.dumps({'club': 'Obj1'}).encode('utf-8') + b'\n'
                            data.outb += response
                        else:
                            print('Unknown request:', req)
                    except json.JSONDecodeError:
                        print("Valami jött, de nem JSON!")
            else:
                print("Closing connection to", data.addr)
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f'Sending {data.outb!r} to {data.addr}')
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
