import logging
import sys
import os

sys.path.append(os.path.dirname(__file__))

from eventhandler import FailLogServer, FailLogClient

ADDR = ('127.0.0.1', 12345)

file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.INFO)
fh = logging.FileHandler("/home/max/Desktop/python/socket_log/test.log")
file_logger.addHandler(fh)

if __name__ == "__main__":
    log_server = FailLogServer(ADDR, [], file_logger)
    log_server.listen()
    log_server.start_loop()