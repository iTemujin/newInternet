import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
message = [b"Message 1 from client.", b"Message 2 from client."]

def request(host, port):
    server_addr = (host, port)

    print(f'Starting connection to {server_addr}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        msg_total=sum(len(m) for m in message),
        recv_total=0,
        messages=message.copy(),
        outb=b"",
    )
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


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(f"Received {recv_data!r} from connection")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data}")
            sel.unregister(sock)
            sock.close()
    
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f'Sending {data.outb!r} to connection {data}')
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
    
