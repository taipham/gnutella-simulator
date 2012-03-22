from pygnutella.bootstrap import RandomBootstrap
from pygnutella.scheduler import loop as schedule_loop, close_all
import logging
import sys

def main(argv, argc):    
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    print "Please use Ctrl+C to terminate"
    p = 0.5
    if argc > 0:
        p = float(argv[0])
    else:
        print "Please provide a argument for possibility [0 - 1]."
        return
    RandomBootstrap(p)
    
    try:
        schedule_loop()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        close_all()
    return
    
if __name__ == "__main__":
    main(sys.argv[1:], len(sys.argv)-1)
