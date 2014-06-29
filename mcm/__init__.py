__author__="tongqg"

import logging

logfile="mcm.log"
level = logging.DEBUG

print('Log message written to {0} at level {1}'.format(logfile, level))
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename=logfile, level=level)
