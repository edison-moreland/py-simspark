import socket
import struct
from .exceptions import NoResponseError


class SimSparkServer(object):
    def __init__(self, host: str, port: int, timeout: int=30, retries: int=5):
        """
        Intermediate class for interacting with SimSpark
        Args:
            host: IP Adresss of the SimSpark server
            port: TCP port of the SimSpark server
            timeout: Time out time in seconds
            retries: Number of times connection can timeout before the connection is closed
        """
        self.address = (host, port)
        self.retries = retries

        # Initialize socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)

    def connect(self):
        """Connect socket to SimSpark server"""
        error = None
        for _ in range(self.retries):  # Keep connecting until successful, or number of retries reached
            try:
                # TODO(LOGGING) log connecting to server
                self.sock.connect(self.address)

                break  # Connection successful, break loop

            except socket.timeout as er:
                # TODO(LOGGING) log retries
                error = er  # Save error to re-raise it later
                continue
        else:
            # TODO(LOGGING) Log failed connection
            raise error

    def disconnect(self):
        """Disconnect socket from SimSpark server"""
        # TODO(LOGGING) Log disconnect from server
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
        prefix = struct.pack("!I", len(payload))  # TODO(ERROR) This should have some error-catching

        # Send message to server
        self.sock.send(prefix + payload)

        # TODO(LOGGING) Log message sent to server

    def receive_message(self):
        """
        Receive message from the server

        Returns:
            str
        """
        # Messages are prefixed with length of payload as a 32 bit unsigned integer
        for i, _ in enumerate(range(self.retries)):
            prefix_raw = self.sock.recv(4)

            try:
                assert prefix_raw != b''  # Throw error if prefix_raw is empty

            except AssertionError:
                # TODO(LOGGING): Log this better
                print("No data returned from server, retrying {}/{}".format(i, self.retries))
                continue  # restart loop if no data from server

            break  # break from loop if server returned data

        else:
            # Never broke from loop, so server never returned data
            raise NoResponseError("No data received from server, is it still running?")

        payload_length = struct.unpack("!I", prefix_raw)

        # get rest of data
        raw_payload = self.sock.recv(payload_length[0])
        payload = raw_payload.decode("ascii")

        # TODO(LOGGING) Log message sent to server
        return payload
