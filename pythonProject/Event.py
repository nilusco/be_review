from MatchTime import MatchTime


class Event:
    def __init__(self, event_type, time: MatchTime, player, obs=""):
        super().__init__()
        self.event_type = event_type
        self.time = time
        self.player = player

    def score(self):
        return 1
