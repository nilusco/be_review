from Rule import Rule
from RuleCondition import ConditionType, RuleCondition
from WrongConditionException import WrongConditionException


class SingleRule(Rule):
    def __init__(self, name, event_type, condition: RuleCondition, points):
        if condition == "at_least":
            raise WrongConditionException("Condition must not be at least")
        self._condition = condition
        super().__init__(name, event_type, points)

    def apply(self, events):
        for event in events:
            if event.event_type == "score":
                if self._condition.type == ConditionType.afterTime:
                    if event.time.is_after(self._condition.value):
                        return self._points
                    else:
                        return 0
                elif self._condition.type == ConditionType.player:
                    return self._points if event.player.is_goalkeeper() else 0
                elif self._condition.type == ConditionType.distance:
                    return self._points if self.goal_in_range(event) else 0

    def goal_in_range(self, event):
        event.obs

