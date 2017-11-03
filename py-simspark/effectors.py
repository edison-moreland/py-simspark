def message_factory(effector_string):
    """Makes messages easy to define"""
    def message(**kwargs):
        return effector_string.format(**kwargs)

    return message


create = message_factory("(scene {filename})")
hinge_joint = message_factory("({name} {ax1})")
universal_joint = message_factory("({name {ax1} {ax2}})")
synchronize = message_factory("(syn)")
init = message_factory("(init (unum {playernumber}) (teamname {teamname}))")
beam = message_factory("(beam {x} {y} {rot})")
say = message_factory("(say {message})")


