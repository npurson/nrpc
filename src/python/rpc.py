import socket
import array
import json
import time

from typing import Tuple


class RPCBase(object):

    def __init__(self, mode='str', headsz=4, bufsz=1024):
        """The base class of RPC sockets.

        Attributes:
            mode: 'str', 'json' or 'array', indicating type of inputs and outputs.
            headsz: header size, maximum length of packets should be below 10 ^ headsz.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        assert mode in [None, 'str', 'json', 'array']
        self.mode = mode
        self.headsz = headsz
        self.bufsz = bufsz
        self.CLOSE_CONNECT = -1
        self.CLOSE_REMOTE = -2

    def _send(self, sock, data):
        data = self.to_bytes(data)
        header = len(data).to_bytes(self.headsz, byteorder='little')
        packet = header + data
        sock.sendall(packet)
        self.logger(('SEND', f'packlen {len(packet)}'))

    def _recv(self, sock, bufsz=1024):
        packet = sock.recv(bufsz)
        if not packet:
            return self.CLOSE_CONNECT, None
        header, data = packet[:self.headsz], packet[self.headsz:]
        header = int.from_bytes(header, 'little', signed=True)
        if header in [self.CLOSE_CONNECT, self.CLOSE_REMOTE]:
            return header, None
        while len(data) != header:
            data += sock.recv(bufsz)
        self.logger(('RECV', f'packlen {self.headsz + len(data)}'))
        return header, self.from_bytes(data)

    def to_bytes(self, data) -> bytes:
        """Converts data to bytes for sending.
        """
        if self.mode is None:
            return data
        elif self.mode == 'str':
            return data.encode()
        elif self.mode == 'json':
            return json.dumps(data)
        elif self.mode == 'array':
            return bytes(data)

    def from_bytes(self, bs: bytes):
        """Interprets received bytes by mode.
        """
        if self.mode is None:
            return bs
        elif self.mode == 'str':
            return bs.decode()
        elif self.mode == 'json':
            return json.loads(bs)
        elif self.mode == 'array':
            a = array.array('d')
            a.frombytes(bs)
            return a

    def logger(self, msg: Tuple[str]):
        """
        Examples:
            >>> self.logger(('CONNECT', 'from remote'))
            2021-01-01 09:01:23 - CONNECT - from remote
        """
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(' - '.join((tm, *msg)))


class Client(RPCBase):

    def __init__(self, addr, port, **kwargs):
        """RPC client."""
        super().__init__(**kwargs)
        self.sock.connect((addr, port))
        self.logger(('CONNECT', f'to {addr}:{str(port)}'))

    def send(self, data):
        self._send(self.sock, data)

    def recv(self):
        return self._recv(self.sock, self.bufsz)

    def close(self):
        self.sock.close()
        self.logger(('CLOSE',))

    def close_connect(self):
        packet = self.CLOSE_CONNECT.to_bytes(self.headsz, byteorder='little', signed=True)
        self.sock.sendall(packet)
        self.close()

    def close_remote(self):
        packet = self.CLOSE_REMOTE.to_bytes(self.headsz, byteorder='little', signed=True)
        self.sock.sendall(packet)
        self.logger(('CLOSE REMOTE',))
        self.close()


class Server(RPCBase):

    def __init__(self, port, **kwargs):
        """RPC server."""
        super(Server, self).__init__(**kwargs)
        self.sock.bind(('localhost', port))
        self.sock.listen(5)
        self.logger(('LISTEN',))

    def recv(self, sock):
        """
        Returns:
            header: data length, CLOSE_CONNECT or CLOSE_REMOTE
            data: message data.
        """
        return self._recv(sock, self.bufsz)

    def send(self, sock, data):
        self._send(sock, data)

    def close(self, sock):
        sock.close()

    def loop(self, callback: callable):
        """Override this method or define the callback function.
        """
        while True:
            conn, addr = self.sock.accept()
            self.logger(('CONNECT', f'from {addr[0]}:{str(addr[1])}'))
            while True:
                header, data = self.recv(conn)
                if header == self.CLOSE_CONNECT:
                    self.close(conn)
                    self.logger(('CLOSE', f'from {addr[0]}:{str(addr[1])}'))
                    break
                elif header == self.CLOSE_REMOTE:
                    self.logger(('EXIT',))
                    return
                else:
                    self.send(conn, callback(data))
