# coding=utf-8
from pprint import pprint
import sexpdata as s_exp

from simspark_server import SimSparkServer

HOST = '192.168.1.166'
PORT = 3100

ssserver = SimSparkServer(host='192.168.1.166',
                          port=3100)
ssserver.connect()

# Initialize nao
ssserver.send_message('(scene rsg/agent/nao/nao.rsg)')
ssserver.send_message('(init (unum 0)(teamname NaoRobot))')

# Make the knee go fast
for _ in range(10):
    ssserver.send_message('(say heyheyhoho)')
    received_message = ssserver.receive_message()

    try:
        preceptors = s_exp.parse(received_message)
    except s_exp.ExpectClosingBracket:
        # S-Expression library sucks, and doesn't sometimes
        preceptors = s_exp.parse(received_message)

    pprint(preceptors)

# Cleanup
ssserver.disconnect()
