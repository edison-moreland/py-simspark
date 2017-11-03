# coding=utf-8
import sys
import random as rand
from agent import BaseAgent

HOST = '192.168.1.166'
PORT = 3100


class ExampleAgent(BaseAgent):
    def run_every_cycle(self, preceptors):
        # Runs every server cycle
        self.say(message="Hello World!")  # Yell at the other teammates

        self.set_hinge_joint(name=rand.choice(["rle1", "rle2", "rle3", "rle4", "rle5", "rle6"]),
                             axis1_speed=rand.randint(-1000, 1000))  # Move right leg randomly

        self.set_hinge_joint(name=rand.choice(["lle1", "lle2", "lle3", "lle4", "lle5", "lle6"]),
                             axis1_speed=rand.randint(-1000, 1000))  # Move left leg randomly

        self.set_hinge_joint(name=rand.choice(["rae1", "rae2", "rae3", "rae4"]),
                             axis1_speed=rand.randint(-1000, 1000))  # Move right arm randomly

        self.set_hinge_joint(name=rand.choice(["lae1", "lae2", "lae3", "lae4"]),
                             axis1_speed=rand.randint(-1000, 1000))  # Move left arm randomly

        print(preceptors)


agent = ExampleAgent(host=HOST, port=PORT, teamname="BestTeam")

try:
    agent.start_cycle()

except(KeyboardInterrupt, SystemExit):
    agent.disconnect()
    sys.exit()
