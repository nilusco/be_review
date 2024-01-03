import unittest

from Event import Event
from MatchTime import MatchTime
from RuleCondition import RuleCondition, ConditionType
from SingleRule import SingleRule

GOAL_EVENT = Event(event_type="score", time=MatchTime("1"), player="Claudio Lopez")
from Partido import Partido
from Torneo import Torneo
from MatchRule import MatchRule
from SideRule import SideRule


class Revisionismo_test_suite(unittest.TestCase):
    def test01_single_game_match_is_won_by_local(self):
        game = Partido("Racing", "Independiente", [GOAL_EVENT], [])

        winner = Torneo([game]).winner()

        self.assertEqual(winner, "Racing")

    def test02_single_game_match_is_won_by_away(self):
        game = Partido("Huracan", "San Lorenzo", [], [GOAL_EVENT])

        winner = Torneo([game]).winner()

        self.assertEqual(winner, "San Lorenzo")

    def test03_tie_game_does_not_have_a_winner(self):
        game = Partido("Boca", "River", [GOAL_EVENT], [GOAL_EVENT])

        winner = Torneo([game]).winner()

        self.assertEqual(winner, "Tie")

    def test04_multiple_games(self):
        game = Partido("Racing", "Independiente", [GOAL_EVENT], [])
        game2 = Partido("Racing", "Independiente", [GOAL_EVENT], [])

        winner = Torneo([game, game2]).winner()

        self.assertEqual(winner, "Racing")

    def test05_win_gives_3_points_for_winner_0_for_loser(self):
        partido = Partido("Racing", "Independiente", [GOAL_EVENT], [])

        score_winner = Torneo([partido]).score("Racing")
        score_loser = Torneo([partido]).score("Independiente")

        self.assertEqual(3, score_winner)
        self.assertEqual(0, score_loser)

    def test05_tied_game_gives_1_point_for_both_teams(self):
        partido = Partido("Racing", "Independiente", [GOAL_EVENT], [GOAL_EVENT])

        score_home = Torneo([partido]).score("Racing")
        score_away = Torneo([partido]).score("Independiente")

        self.assertEqual(1, score_home)
        self.assertEqual(1, score_away)

    def test06_2_points_rule_gives_2_points_to_winner(self):
        partido = Partido("Racing", "Independiente", [GOAL_EVENT], [])
        two_point_win_rule = MatchRule("match_rule", "win", points=2)

        score_home = Torneo(partidos=[partido], rules=[two_point_win_rule]).score("Racing")
        score_away = Torneo([partido]).score("Independiente")

        self.assertEqual(2, score_home)
        self.assertEqual(0, score_away)

    def test07_side_rule_gives_extra_point_to_home_team_with_more_than_3_goals(self):
        home_events = [GOAL_EVENT, Event(event_type="score", time=MatchTime("2"), player="Claudio Lopez"),
                       Event(event_type="score", time=MatchTime("3"), player="Claudio Lopez")]
        partido = Partido("Racing", "Independiente", home_events, [])
        side_rule = SideRule("side_rule", event_type="score", repetitions=3, points=1)

        score_home = Torneo(partidos=[partido], side_rules=[side_rule]).score("Racing")

        self.assertEqual(4, score_home)

    def test08_side_rule_gives_extra_point_to_away_team_with_more_than_3_goals(self):
        events = [GOAL_EVENT, Event(event_type="score", time=MatchTime("2"), player="Claudio Lopez"),
                  Event(event_type="score", time=MatchTime("3"), player="Claudio Lopez")]
        partido = Partido("Racing", "Independiente", [], events)
        side_rule = SideRule("side_rule", event_type="score", repetitions=3, points=1)

        score_away = Torneo(partidos=[partido], side_rules=[side_rule]).score("Independiente")

        self.assertEqual(4, score_away)

    def test09_side_rule_gives_extra_point_to_team_that_saved_a_penalty(self):
        events = [GOAL_EVENT, Event(event_type="pk_save", time=MatchTime("1"), player="")]
        partido = Partido("Racing", "Independiente", events, [])
        side_rule = SideRule("side_rule", event_type="pk_save", repetitions=1, points=1)

        score = Torneo(partidos=[partido], side_rules=[side_rule]).score("Racing")

        self.assertEqual(4, score)

    def test10_single_rule_gives_extra_point_to_team_that_saved_a_penalty(self):
        events = [Event(event_type="score", time=MatchTime("90 +1"), player="Chris")]
        partido = Partido("Racing", "Independiente", events, [])
        single_rule = SingleRule(name="single_rule", event_type="score", condition=RuleCondition(ConditionType.afterTime, MatchTime("90 +0")), points=1)

        score = Torneo(partidos=[partido], single_rules=[single_rule]).score("Racing")

        self.assertEqual(4, score)


    def test11_tournament_summary_has_ammount_of_matches_played(self):
        game = Partido("Racing", "Independiente", [GOAL_EVENT], [])

        summary = Torneo([game]).summary()

        self.assertEqual(summary["Racing"]["matches"], 1)
        self.assertEqual(summary["Independiente"]["matches"], 1)

    def test12_tournament_summary_has_ammount_of_goals(self):
        game = Partido("Racing", "Independiente", [GOAL_EVENT], [])

        summary = Torneo([game]).summary()

        self.assertEqual(summary["Racing"]["goals"], 1)
        self.assertEqual(summary["Independiente"]["goals"], 0)

    def test13_tournament_summary_has_bonus_points(self):
        events = [GOAL_EVENT, Event(event_type="score", time=MatchTime("2"), player="Claudio Lopez"),
                  Event(event_type="score", time=MatchTime("3"), player="Claudio Lopez")]
        partido = Partido("Racing", "Independiente", [], events)
        side_rule = SideRule("side_rule", event_type="score", repetitions=3, points=1)

        summary = Torneo(partidos=[partido], side_rules=[side_rule]).summary()

        self.assertEqual(summary["Racing"]["bonus_points"], 1)
        self.assertEqual(summary["Independiente"]["bonus_points"], 0)


if __name__ == '__main__':
    unittest.main()
