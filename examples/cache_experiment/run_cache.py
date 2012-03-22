from pygnutella.network import create_network
from pygnutella.servent import BasicServent, FileInfo
import sys

def usage():
    print "Please run with <bootstrap ip> <bootstrap port> <num of nodes> <num of nodes have the file>"

def __create_node(servent_cls, bootstrap_address, files = []):
    pass

def main(args):
    if len(args)<4:
        usage();
        return
    ip = args[0]
    port = int(args[1])
    num_node = int(args[2])
    # number of node having the file is at least 1
    num_node_have_file = max(int(args[3]),1)
    files = [FileInfo(1,"ABC",1)]            
    address = (ip, port)

if __name__ == '__main__':
    main(sys.argv[1:])