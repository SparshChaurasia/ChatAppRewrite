from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def connectionMade(self):
        print("New connection")
        self.transport.write("An apple a day keeps the doctor away".encode("utf-8"))
        self.transport.loseConnection()

class ServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return Server()


if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9999)
    endpoint.listen(ServerFactory())
    reactor.run()