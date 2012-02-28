from pygnutella.reactor import Reactor
from pygnutella.message import Message
from pygnutella.messagebody import PingBody
import logging
import sys

def connector(connection_handler):
    print "connecting %s", connection_handler.socket.getsockname()
    msg = Message('somemsgid')
    PingBody(msg)
    connection_handler.send_message(msg)
    
def acceptor():
    return True

def disconnector(connection_handler):
    print "disconnected"

def receiver(connection_handler, message):
    print "receiving message = ", message.serialize()
    print "message len = ", len(message.serialize())
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')                        
    reactor = Reactor()
    reactor.install_handlers(acceptor, connector, receiver, disconnector)
    if len(sys.argv) > 2:
        reactor.make_outgoing_connection((sys.argv[1], int(sys.argv[2])))
    reactor.run()