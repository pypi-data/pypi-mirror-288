class MockGPIO:
    BCM = 'BCM'
    BOARD = 'BOARD'
    OUT = 'OUT'
    IN = 'IN'
    PUD_UP = 'PUD_UP'
    HIGH = True
    LOW = False

    def __init__(self):
        self.mode = None
        self.pins = {}

    def setmode(self, mode):
        self.mode = mode

    def setup(self, channel, mode, pull_up_down=None):
        self.pins[channel] = {
            'mode': mode,
            'state': self.LOW,
            'pull_up_down': pull_up_down
        }

    def output(self, channel, state):
        if channel in self.pins and self.pins[channel]['mode'] == self.OUT:
            self.pins[channel]['state'] = state

    def input(self, channel):
        if channel in self.pins and self.pins[channel]['mode'] == self.IN:
            return self.pins[channel]['state']
        return self.LOW

    def cleanup(self):
        self.pins = {}

GPIO = MockGPIO()