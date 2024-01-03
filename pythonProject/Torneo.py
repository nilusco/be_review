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
        self._matches_played = {}
        self._goals = {}
        self._single_rules = single_rules
        self.score_championship()

    def score_championship(self):
        for partido in self._partidos:
            self._record_match(partido)

    def _record_match(self, partido):
        points_for_teams = partido.score_match(self.rules, self._side_rules, self._single_rules)
        for team, points in points_for_teams.items():
            self._scores[team] = self._scores.get(team, 0) + points[0]
            self._matches_played[team] = self._matches_played.get(team, 0) + 1
            self._goals[team] = self._goals.get(team, 0) + points[1]

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
            rules.append(MatchRule("match_rule", event_type, points))

    def summary(self):
        summary = {}
        for team, points in self._scores.items():
            summary[team] = {"points": points, "matches": self._matches_played[team], "goals": self._goals[team]}

        return summary
