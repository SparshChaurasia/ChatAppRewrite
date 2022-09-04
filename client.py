from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as BaseClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

class Client(Protocol):
    def __init__(self):
        reactor.callInThread(self.send_message)

    def dataReceived(self, data):
        data = data.decode("utf-8")
        print(data)

    def send_message(self):
        while True:
            msg = input().encode("utf-8")
            self.transport.write(msg)


class ClientFactory(BaseClientFactory):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        BaseClientFactory.clientConnectionFailed(self, connector, reason)
    
    def clientConnectionLost(self, connector, reason):
        print(reason)
        BaseClientFactory.clientConnectionLost(self, connector, reason)


if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, "localhost", 9999)
    endpoint.connect(ClientFactory())
    reactor.run()
