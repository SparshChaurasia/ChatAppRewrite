from twisted.internet import reactor
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as BaseServerFactory 
from twisted.internet.endpoints import TCP4ServerEndpoint
from enum import Enum

State = Enum('state', 'GETNAME CHAT')

class Server(Protocol):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = State.GETNAME

    def connectionMade(self):
        print("New connection")
        self.transport.write("Hello from server!\nPlease enter your name".encode("utf-8"))

    def connectionLost(self, reason=connectionDone):
        del self.users[self.name]

    def dataReceived(self, data):
        if self.state == State.GETNAME:
            self.handle_getname(data)
        else:
            self.handle_chat(data)
    
    def handle_getname(self, name):
        if name in self.users:
            self.transport.write("Name is taken chose another!")
        
        self.name = name
        self.users[name] = self

        print(self.name.decode("utf-8"), "joined the chat!")
        self.state= State.CHAT

    def handle_chat(self, data):
        for name, conn in self.users.items():
            if name == self.name:
                continue
            conn.transport.write(self.name + data)

class ServerFactory(BaseServerFactory):
    def __init__(self):
        self.users = {}
        print("Server started!")

    def buildProtocol(self, addr):
        return Server(self.users)


if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9999)
    endpoint.listen(ServerFactory())
    reactor.run()