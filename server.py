from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as BaseServerFactory 
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def __init__(self, users):
        self.users = users

    def connectionMade(self):
        print("New connection")
        self.transport.write("Hello from server".encode("utf-8"))
        self.users.append(self)

    def dataReceived(self, data):
        for user in self.users:
            if user == self:
                continue
            user.transport.write(data)

class ServerFactory(BaseServerFactory):
    def __init__(self):
        self.users = []

    def buildProtocol(self, addr):
        return Server(self.users)


if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9999)
    endpoint.listen(ServerFactory())
    reactor.run()