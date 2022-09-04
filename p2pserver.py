from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class RendezvousServer(DatagramProtocol):
    def __init__(self):
        self.clients = set()

    def datagramReceived(self, datagram, addr):
        res = datagram.decode("utf-8")
        if res == "ready":
            clients = ",".join([str(x) for x in self.clients]) 

            self.transport.write(clients.encode("utf-8"), addr)
            self.clients.add(addr)


if __name__ == "__main__":
    reactor.listenUDP(9999, RendezvousServer())
    reactor.run()
