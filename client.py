import sys
import socket
import selectors
import types
import json

sel = selectors.DefaultSelector()

def request(host, port):
    server_addr = (host, port)

    print(f'Starting connection to {server_addr}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        outb=b"",
        recv_buf=b"",
        result=[],
    )

    # Küldésre kerülő kérés (newline-delimitált JSON)
    json_data = json.dumps({'request': 'get_club'}).encode('utf-8') + b'\n'
    data.outb = json_data

    sel.register(sock, events, data=data)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                service_connection(key, mask)

            if not sel.get_map():
                break

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

    return data.result[0] if data.result else None


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(4096)
        if recv_data:
            data.recv_buf += recv_data
            while b'\n' in data.recv_buf:
                line, data.recv_buf = data.recv_buf.split(b'\n', 1)
                try:
                    parsed = json.loads(line.decode('utf-8'))
                    data.result.append(parsed)
                    sel.unregister(sock)
                    sock.close()
                    return
                except json.JSONDecodeError:
                    print('Received invalid JSON from server')
        else:
            sel.unregister(sock)
            sock.close()
            return

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
