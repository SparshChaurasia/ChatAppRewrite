import pickle

from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as BaseClientFactory

from utility import Message


class Client(Protocol):
    def __init__(self, console):
        self.STDOUT = console

        reactor.callInThread(self.send_message)

    def dataReceived(self, data):
        msg = pickle.loads(data)
        if msg.author == "SERVER":
            self.STDOUT.rule(msg.msg)
            return
        self.STDOUT.print(str(msg))

    def send_message(self):
        while True:
            _msg = input()
            msg = Message(_msg).encode_msg()
            self.transport.write(msg)


class ClientFactory(BaseClientFactory):
    def __init__(self, console: Console):
        self.console = console

    def buildProtocol(self, addr):
        return Client(self.console)

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        BaseClientFactory.clientConnectionFailed(self, connector, reason)
    
    def clientConnectionLost(self, connector, reason):
        print(reason)
        BaseClientFactory.clientConnectionLost(self, connector, reason)


if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, "localhost", 9999)

    console = Console()
    clFactory = ClientFactory(console)

    endpoint.connect(clFactory)
    reactor.run()
