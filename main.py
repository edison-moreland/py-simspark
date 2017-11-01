# coding=utf-8
# terrible example agent from wiki

import socket
import struct
import sexpdata
HOST = 'localhost'
PORT = 3100


def send_effector(msg):
    """
    Each message is prefixed with the length of the payload message.
    The length prefix is a 32 bit unsigned integer in network order
    """
    msg = msg.encode("ascii")
    sock.send(struct.pack("!I", len(msg)) + msg)


def recieve_perceptors():
    # get header
    length_no = sock.recv(4)
    length = struct.unpack("!I", length_no)

    # get rest of data
    sexprstr = sock.recv(length[0])
    perceptors = sexpdata.dumps(sexprstr)

    return perceptors


print("connecting to server")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("initialising")
send_effector('(scene rsg/agent/nao/nao.rsg)')
print(sock.recv(1024))
send_effector('(init (unum 0)(teamname NaoRobot))')
print(sock.recv(1024))
send_effector('(he1 1)')
print(sock.recv(1024))