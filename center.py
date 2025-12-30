from identity import Identity
from server import Server

import threading
import queue

import time

posta = queue.Queue()
identity_posta = queue.Queue()

def run():
    threading.Thread(target=runServer, args=(posta, identity_posta,)).start()
    ip = posta.get()
    print(f"Obtained IP: {ip}")
    identity = Identity(ip)
    identity_posta.put(identity)

    while True:
        None


def runServer(posta, identity_posta):
    src = Server(posta=posta, identity_posta=identity_posta)
    print('run')

    threading.Thread(target=src._run_tagHere, daemon=True).start()
    src.run()
    print("Leallt")

if __name__ == "__main__":
    run()