from twisted.internet import reactor
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as BaseServerFactory 
from twisted.internet.endpoints import TCP4ServerEndpoint
from enum import Enum
from utility import Message
import pickle

State = Enum('state', 'GETNAME CHAT')

class Server(Protocol):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = State.GETNAME

    def connectionMade(self):
        print("New connection")
        msg = Message("Hello from server!\nPlease enter your name").encode_msg()
        self.transport.write(msg)

    def connectionLost(self, reason=connectionDone):
        del self.users[self.name]

        _msg = f"{self.name} left the chat!"
        msg = Message(_msg).encode_msg()

        print(_msg)
        self.handle_chat(msg)

    def dataReceived(self, data):
        if self.state == State.GETNAME:
            self.handle_getname(data)
        else:
            self.handle_chat(data)
    
    def handle_getname(self, data):
        name = pickle.loads(data).msg

        if name in self.users:
            msg = Message("Name is taken chose another!").encode_msg()
            self.transport.write(msg)
        
        self.name = name
        self.users[name] = self

        _msg = f"{self.name} joined the chat!"
        msg = Message(_msg).encode_msg()

        print(_msg)
        self.handle_chat(msg)

        self.state = State.CHAT

    def handle_chat(self, data):
        for name, conn in self.users.items():
            if name == self.name:
                continue
            conn.transport.write(data)

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