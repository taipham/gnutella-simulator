import sys
from pygnutella.servent import FileInfo
from pygnutella.demo.cache_servent import CacheServent
from pygnutella.scheduler import loop as scheduler_loop, close_all

def main(args):
    # implement the network
    servent1 = CacheServent()
    servent2 = CacheServent()
    servent3 = CacheServent()
    servent4 = CacheServent()
    servent5 = CacheServent()
    servent3.set_files([FileInfo(1,"first file", 600),
                       FileInfo(2,"second file", 2500) ,
                       FileInfo(3, "third file", 5000)])
    servent1.reactor.gnutella_connect(servent2.reactor.address)
    servent2.reactor.gnutella_connect(servent3.reactor.address)
    servent3.reactor.gnutella_connect(servent4.reactor.address)
    servent5.reactor.gnutella_connect(servent2.reactor.address)
    try:
        scheduler_loop(timeout=1,count=10)
    finally:
        #flood is query to neighbors
        #servent1.query_flood('first file')
        scheduler_loop(timeout=1,count=10)
        print "============NEXT QUERY============"
        # servent2.query_flood('first file')
        # scheduler_loop(timeout=1,count=10)
        #servent5.query_flood('first file')
        scheduler_loop(timeout=1,count=15)
        close_all()


if __name__ == '__main__':
    main(sys.argv[1:])