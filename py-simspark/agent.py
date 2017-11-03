from simspark_server import SimSparkServer
import effectors as ef


class BaseAgent(SimSparkServer):
    model_path = "rsg/agent/nao/nao.rsg"  # Defaults to Nao model

    def __init__(self, teamname: str, player_number: int=0, host: str="localhost", port: int=3100):
        """

        Args:
            teamname: Name of team to join, creates new team if it doesn't exist
            player_number: Position on team, auto selects number if 0
            host: address of server
            port: tcp port of server
        """
        super().__init__(host=host, port=port)
        self.teamname = teamname
        self.player_number = player_number

        self.cycle_message = ""

    # Commands
    def synchronize(self):
        """Sent after every cycle of the server if AgentSyncMode is enabled, auto appended after every cycle"""
        self.cycle_message += ef.synchronize()

    def set_hinge_joint(self, name: str, axis1_speed: float):
        """
        Sets speed of axis on hinge joint

        Args:
            name: Name of joint to set
            axis1_speed: Speed value to set on axis, in radians per second. Speed will be maintained until new value set
        """
        self.cycle_message += ef.hinge_joint(name=name, ax1=axis1_speed)

    def set_universal_joint(self, name: str, axis1_speed: float, axis2_speed: float):
        """
        Sets speed of axises on universal joint

        Args:
            name: Name of joint to set
            axis1_speed: Speed value to set on axis, in radians per second. Speed will be maintained until new value set
            axis2_speed: Speed value to set on axis, in radians per second. Speed will be maintained until new value set
        """
        self.cycle_message += ef.universal_joint(name=name, ax1=axis1_speed, ax2=axis2_speed)

    def beam(self, x_pos: float, y_pos: float, direction: float):
        """
        Set player position at beginning of each half. Middle of field is 0,0

        Args:
            x_pos: X coordinate of player
            y_pos: Y coordinate of player
            direction: Direction of player. 0 points to +X axis, 90 points to +Y axis
        """
        self.cycle_message += ef.beam(x=x_pos, y=y_pos, rot=direction)

    def say(self, message):
        """
        Broadcast message to other agents

        Args:
            message: message to broadcast
        """
        self.cycle_message += ef.say(message=message)

    # Server stuff
    def _parse_preceptors(self, raw_preceptors):
        """Takes raw preceptor data and gives usable data"""
        # TODO(PRECEPTORS) Find a good S-Expression to parse response from the server
        return raw_preceptors

    def _initialize_on_server(self):
        """Creates player model, and registers on a team"""
        self.send_message(ef.create(filename=self.model_path))
        self.send_message(ef.init(playernumber=self.player_number,
                                  teamname=self.teamname))

    def run_every_cycle(self, preceptors):
        """Runs every cycle after getting preceptors from the server"""
        self.synchronize()

    def start_cycle(self):
        """
        Initializes agent with the server and starts agent loop
        """
        self.connect()
        self._initialize_on_server()

        while True:
            # Get and process preceptors data from server
            preceptor_data = self._parse_preceptors(self.receive_message())

            # Prepare actions for next cycle
            self.run_every_cycle(preceptors=preceptor_data)

            # Append sync message
            self.synchronize()

            # Send entire message
            self.send_message(self.cycle_message)

            # Prepare for next cycle
            self.cycle_message = ""
