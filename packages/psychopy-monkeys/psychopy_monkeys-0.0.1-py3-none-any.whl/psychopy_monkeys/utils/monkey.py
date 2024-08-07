from psychopy import constants


class Monkey:
    """
    Class which simply holds information (status, associated input, time started/stopped, etc.) 
    about a PsychoPy Monkey Component.
    """
    def __init__(self, name="", comp=None):
        # store ref to associated Component
        self.comp = comp
        # start value for status
        self.status = constants.NOT_STARTED