from unittest import result

from MatchRule import MatchRule


class Partido:
    def __init__(self, home, away, home_events, away_events):
        super().__init__()
        self.home = home
        self.away = away
        self.home_events = home_events
        self.away_events = away_events

        self.home_goals = sum(event.score() for event in home_events)
        self.away_goals = sum(event.score() for event in away_events)

    def score_match(self, rules, side_rules, single_rules):

        scores = self.score_match_result(rules + side_rules + single_rules)
        home_points = scores[0]
        away_points = scores[1]
#        self.score_side_rules(result, side_rules)
#        self.score_single_rules(result, single_rules)

        return {self.home: [home_points, self.home_goals], self.away: [away_points, self.away_goals]}

    def score_side_rules(self, result, side_rules):
        for side_rule in side_rules:
            side_rule(self.home_events)

        for side_rule in side_rules:
            home_repetitions = sum(
                1 for home_event in self.home_events if home_event.event_type == side_rule.event_type)
            if home_repetitions >= side_rule.repetitions:
                result[self.home] = result[self.home] + side_rule.points

            away_repetitions = sum(
                1 for away_event in self.away_events if away_event.event_type == side_rule.event_type)
            if away_repetitions >= side_rule.repetitions:
                result[self.away] = result[self.away] + side_rule.points

    def score_match_result(self, rules):
        scores = [rule.apply(self.home_events, self.away_events) for rule in rules]
        total_scores = [sum(x) for x in zip(*scores)]
        return total_scores
#        for rule in rules:
#            rule.apply(self.home_events, self.away_events)

        # if self.home_score > self.away_score:
        #     return {self.home: self._victory_rule.victory_points(), self.away: self._lose_rule.loser_points()}
        # else:
        #     if self.home_score < self.away_score:
        #         return {self.away: self._victory_rule.victory_points(), self.home: self._lose_rule.loser_points()}
        # return {self.home: self._tie_rule.tie_points(), self.away: self._tie_rule.tie_points()}

    def score_single_rules(self, result, single_rules):
        for single_rule in single_rules:
            event_to_check = [event for event in self.home_events if event.event_type == single_rule.event_type]
