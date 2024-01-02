from collections import defaultdict

from MatchRule import MatchRule
from Rule import Rule


class Torneo:
    def __init__(self, partidos, rules=[], side_rules=[], single_rules=[]):
        super().__init__()
        self.rules = self._initialize_match_rules(rules)

        self._side_rules = side_rules
        self._partidos = partidos
        self._scores = {}
        self._single_rules = single_rules
        self.score_championship()

    def score_championship(self):
        for partido in self._partidos:
            points_for_teams = partido.score_match(self._reglas, self._side_rules, self._single_rules)
            for team, points in points_for_teams.items():
                self._scores[team] = self._scores.get(team, 0) + points

    def winner(self):
        max_points = 0
        for key in self._scores.keys():
            champion = key

        for team, score in self._scores.items():
            if score > max_points:
                champion = team

        if len(self._scores.keys()) > 0:
            return champion
        return "Tie"

    def score(self, team):
        return self._scores.get(team, 0)

    def _initialize_match_rules(self, rules: [Rule]):
        self.check_rule_existence(rules, "win", 3)
        self.check_rule_existence(rules, "loss", 0)
        self.check_rule_existence(rules, "tie", 1)
        return rules

    def check_rule_existence(self, rules, event_type, points):
        filtered_rules = list(filter(lambda r: r._event_type == event_type, rules))
        if len(filtered_rules) == 0:
            rules.append(Rule("match_rule", event_type, points))
