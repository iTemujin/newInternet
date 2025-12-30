import socket

def find_server(port=5005):
    # UDP socket létrehozása
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)
    
    message = b"DISCOVER_SERVER"
    print("Szerver keresése...")
    
    # Broadcast küldése mindenkihez a hálózaton
    sock.sendto(message, ('<broadcast>', port))
    
    try:
        data, addr = sock.recvfrom(1024)
        if data == b"SERVER_HERE":
            print(f"Szerver megtalálva! IP: {addr[0]}")
            return addr[0]
    except socket.timeout:
        print("Nem található szerver a hálózaton.")
    finally:
        sock.close()

# Használat:
if __name__ == "__main__":
    server_ip = find_server()