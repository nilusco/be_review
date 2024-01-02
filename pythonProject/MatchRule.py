from Rule import Rule


class MatchRule(Rule):
    def apply(self, events):
        pass

    def __init__(self, name, event, points=3):
        super().__init__(name, event, points)

