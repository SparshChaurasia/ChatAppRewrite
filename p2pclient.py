from enum import Enum

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

State = Enum('state', 'GETPEER CHAT')

class P2PClient(DatagramProtocol):
    def __init__(self, host, port):
        self.id = (host, port)
        self.peer = None
        self.rendezvous_server = ("127.0.0.1", 9999)
        self.state = State.GETPEER

        print("Working on id: ", self.id)

    def startProtocol(self):
        msg = "ready".encode("utf-8")
        self.transport.write(msg, self.rendezvous_server)

    def datagramReceived(self, datagram, addr):
        if self.state == State.GETPEER:
            self.handle_getpeer(datagram, addr)
        else:
            self.handle_chat(datagram, addr)

    def handle_getpeer(self, datagram, addr):
        data = datagram.decode("utf-8")

        print("Chose a peer to connect", data)
        self.peer = input("enter host: "), int(input("enter port: "))
        reactor.callInThread(self.send_messages)
        self.state = State.CHAT


    def handle_chat(self, datagram, addr):
        print(f"{addr}: {datagram}")


    def send_messages(self):
        while True:
            msg = input().encode("utf-8")
            self.transport.write(msg, self.peer)

if __name__ == "__main__":
    port = int(input("Enter port number: "))
    reactor.listenUDP(port, P2PClient("127.0.0.1", port))
    reactor.run()
