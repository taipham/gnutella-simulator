from pygnutella.servent import FileInfo
from pygnutella.demo.cache_servent import CacheServent
from pygnutella.message import create_message
from pygnutella.messagebody import GnutellaBodyId
from numpy.random import randint
import sys, logging
from time import sleep
from multiprocessing import Process
from pygnutella.scheduler import loop as schedule_loop, close_all

class ExperimentServent(CacheServent):
    def __init__(self, bootstrap_address = None):
        CacheServent.__init__(self, bootstrap_address)
        # number of transmitted message include flood[_ex], forward, and send_message 
        self.num_tx_message = 0
        # number of received message
        self.num_rx_message = 0
        # expect query message_id
        self.query_message_id = None
        
    def on_receive(self, connection_handler, message):
        # increase received message by one
        self.num_rx_message += 1
        CacheServent.on_receive(self, connection_handler, message)
        
    def send_message(self, message, handler):
        self.num_tx_message += 1
        CacheServent.send_message(self, message, handler)        
        
    def forward(self, message):
        ret = CacheServent.forward(self, message)
        if ret:
            self.num_tx_message += 1
        return ret
    
    def flood(self, connection_handler, message):
        ret = CacheServent.flood(self, connection_handler, message) 
        self.num_tx_message += ret
        return ret

    def flood_ex(self, message):
        ret = CacheServent.flood_ex(self, message)
        self.num_tx_message += ret
        return ret

    def send_query_to_network(self):
        """
        This is core of the experiment
        """
        # check if we already host the file
        # we hardcode the file name (doesn't really matter)
        criteria = 'ABC' 
        result = self.search(criteria)
        cache_result = self.search_queryhit(criteria)
        if result == [] and cache_result == []:
            # if it is not in cache or not host it
            query_message = create_message(GnutellaBodyId.QUERY,
                                            min_speed = 0,
                                            search_criteria = criteria)
            self.flood_ex(query_message)

def usage():
    print "Please run with <bootstrap ip> <bootstrap port> <num of nodes> <num of nodes have the file>"

def __create_node(servent_cls, bootstrap_address, files = []):
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    servent = servent_cls(bootstrap_address = bootstrap_address)
    servent.set_files(files = files)
    
    try:
        schedule_loop()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        close_all()  

def main(args):
    if len(args)<4:
        usage();
        return
    ip = args[0]
    port = int(args[1])
    num_node = int(args[2])
    # number of node having the file is at least 1
    num_node_have_file = max(int(args[3]),1)
    
    if num_node < num_node_have_file:
        print "number of nodes must be less than number of nodes having the file"
        return
    
    # random generate which node have the file initially
    node_have_file = []
    for _ in xrange(0, num_node_have_file):
        while True:
            node = randint(0, num_node)
            if node not in node_have_file:
                node_have_file.append(node)
                break         
    
    # preparing the file list and address
    files = [FileInfo(1,"ABC",1)]            
    address = (ip, port)
    
    # start simulating
    print "Please use Ctrl+C to terminate"
    children = []
    try:
        # start the node
        for node in xrange(0, num_node):
            if node in node_have_file:
                p = Process(target = __create_node, args=(ExperimentServent, address, files))
            else:
                p = Process(target = __create_node, args=(ExperimentServent, address))
            children.append(p)
            p.start()
            # sleep 1 seconds before start another node
            sleep(1)
        # wait for other process                    
        for p in children:
            p.join()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        for p in children:
            try:
                p.terminate()
                p.join()
            except:
                pass

if __name__ == '__main__':
    main(sys.argv[1:])