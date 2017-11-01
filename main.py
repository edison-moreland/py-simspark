# coding=utf-8
# !/usr/bin/python

import socket
import struct
import sexpdata


def send_effector(msg):
    '''Each message is prefixed with the length of the payload message.
    The length prefix is a 32 bit unsigned integer in network order'''
    print("S:", msg)
    sock.send(struct.pack("!I", len(msg)) + msg.encode("ascii"))


def recieve_perceptors():
    length_no = sock.recv(4)
    length = struct.unpack("!I", length_no)
    sexprstr = sock.recv(length[0])
    sexprlist = sexpdata.dumps(sexprstr)
    perceptors = {}
    for subl in sexprlist:
        if ('HJ' in subl):
            perceptors[subl[1][1]] = float(subl[2][1])

    print("R: hj1", perceptors["hj1"], "\n")
    return perceptors


HOST = 'localhost'
PORT = 3100
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

send_effector('(scene rsg/agent/nao/nao.rsg)')
recieve_perceptors()
send_effector('(init (unum 0)(teamname NaoRobot))')
recieve_perceptors()
send_effector('(he1 1)')
perceptors = recieve_perceptors()

while True:
    if (perceptors["hj1"] > 120.0):
        send_effector('(he1 -1)')

    if (perceptors["hj1"] < -120):
        send_effector('(he1 1)')

    perceptors = recieve_perceptors()