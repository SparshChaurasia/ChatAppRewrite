import pickle
from enum import Enum

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as BaseServerFactory
from twisted.internet.protocol import connectionDone

from utility import Message

State = Enum("state", "GETNAME CHAT")


class Server(Protocol):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = State.GETNAME

    def connectionMade(self):
        print("New connection")
        msg = Message("Enter your username for the server.", "SERVER").encode_msg()
        self.transport.write(msg)

    def connectionLost(self, reason=connectionDone):
        if self.name not in self.users.keys():
            return

        del self.users[self.name]

        _msg = f"{self.name} left the chat!"
        msg = Message(msg=_msg, mtype="MSG")

        print(_msg)
        self.handle_chat(msg, "SERVER")

    def dataReceived(self, data):
        data = pickle.loads(data)
        author = self.name

        if self.state == State.GETNAME:
            self.handle_getname(data)
        else:
            self.handle_chat(data, author)

    def handle_getname(self, data):
        name = data.msg

        if name in self.users.keys() or name == "SERVER":
            msg = Message("Name is taken chose another!", "SERVER").encode_msg()
            self.transport.write(msg)
            return

        self.name = name
        self.users[name] = self

        _msg = f"{self.name} joined the chat!"
        msg = Message(msg=_msg, mtype="MSG")

        print(_msg)
        self.handle_chat(msg, "SERVER")

        self.state = State.CHAT

    def handle_chat(self, msg, author=None):
        if author != None:
            msg.author = author

        for name, conn in self.users.items():
            if name == self.name:
                continue
            conn.transport.write(msg.encode_msg())


class ServerFactory(BaseServerFactory):
    def __init__(self):
        self.users = {}
        print("Server started!")

    def buildProtocol(self, addr):
        return Server(self.users)


if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9999, interface="localhost")
    endpoint.listen(ServerFactory())
    reactor.run()
