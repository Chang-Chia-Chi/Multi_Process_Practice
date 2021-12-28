import logging, logging.handlers

ADDR = ('127.0.0.1', 12345)

def sock_log_test():
    socket_logger = logging.getLogger("socket_logger")
    socket_logger.setLevel(logging.INFO)
    sh = logging.handlers.SocketHandler(*ADDR)
    socket_logger.addHandler(sh)
    for i in range(30):
        socket_logger.info("{} time log".format(i))
    sh.close()

if __name__ == "__main__":
    sock_log_test()
