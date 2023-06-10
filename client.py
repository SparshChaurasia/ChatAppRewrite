import pickle
import sys

from rich.console import Console
from rich.markdown import Markdown
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
        message = pickle.loads(data)
        if message.mtype == "MSG":
            self.STDOUT.rule(message.msg)
        elif message.mtype == "MD":
            md = Markdown(message.msg)
            self.STDOUT.print(
                f"[bold][red]\[{message.timestamp.strftime('%H:%M')}][/][green]\[{message.author}][/][/]"
            )
            self.STDOUT.print(md)
        else:
            self.STDOUT.print(str(message))

    def send_message(self):
        while True:
            # msg = input()

            _msg = []
            line = " "
            while line != "":
                line = input()
                _msg.append(line)

            msg = "\n".join(_msg).strip()
            message = Message(msg, mtype="MD").encode_msg()
            self.transport.write(message)


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
