from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as BaseServerFactory 
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def connectionMade(self):
        print("New connection")
        self.transport.write("Hello from server".encode("utf-8"))

    def dataReceived(self, data):
        print(data.decode("utf-8"))
        self.transport.write(data)

class ServerFactory(BaseServerFactory):
    def buildProtocol(self, addr):
        return Server()


if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9999)
    endpoint.listen(ServerFactory())
    reactor.run()