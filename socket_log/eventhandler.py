import logging, logging.handlers
import pickle
import socket
import select
import struct
import threading

class EventLoop:
    def start_loop(self):
        while True:
            readible, writable, _ = select.select(self.read_handlers, self.write_handlers, [])
            for r in readible:
                r.handle_read()
            for w in writable:
                w.handle_write()

class TCPHandler:
    def fileno(self):
        return self.socket.fileno()
        
    def handle_read(self):
        pass

    def handle_write(self):
        pass

class FailLogServer(TCPHandler, EventLoop):
    def __init__(self, addr, write_handlers, file_logger):
        self._addr = addr
        self.read_handlers = [self]
        self.write_handlers = write_handlers
        self.file_logger = file_logger
    
    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind(self._addr)
        self.socket.listen()

    def handle_read(self):
        client, _ = self.socket.accept()
        self.write_handlers.append(FailLogClient(client, self.write_handlers, self.file_logger))

class FailLogClient(TCPHandler):

    def __init__(self, socket, write_handlers, file_logger):
        self.socket = socket
        self.write_handlers = write_handlers
        self.file_logger = file_logger

    def close(self):
        if hasattr(self, 'socket'):
            self.socket.close()
        self.write_handlers.remove(self)

    def handle_write(self):
        query = self._recv_log()
        if not query:
            self.close()
        self.file_logger.info(query)

    def unpickle(self, data):
        return pickle.loads(data)

    def _recv_log(self):
        """
        https://docs.python.org/2.4/lib/network-logging.html
        """
        while True:
            chunk = self.socket.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.socket.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.socket.recv(slen - len(chunk))
            obj = self.unpickle(chunk)
            return logging.makeLogRecord(obj)