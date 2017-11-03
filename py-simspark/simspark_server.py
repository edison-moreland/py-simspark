import socket
import struct


class SimSparkServer(object):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connect socket to SimSpark server"""
        self.sock.connect((self.host, self.port))

    def disconnect(self):
        """Disconnect socket from SimSpark server"""
        self.sock.close()

    def send_message(self, msg: str):
        """
        Send message to server

        Args:
            msg (str): s-encoded message
        """
        # Messages have to be encoded in ASCII
        payload = msg.encode("ascii")

        # Messages are prefixed with length of payload as a 32 bit unsigned integer
        prefix = struct.pack("!I", len(payload))

        # Send message to server
        self.sock.send(prefix + payload)

    def receive_message(self):
        """
        Receive message from the server

        Returns:
            str
        """
        # get header
        prefix_raw = self.sock.recv(4)
        payload_length = struct.unpack("!I", prefix_raw)

        # get rest of data
        raw_payload = self.sock.recv(payload_length[0])
        assert isinstance(raw_payload, bytes)
        payload = raw_payload.decode("ascii")

        return payload
