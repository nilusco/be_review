import string


class MatchTime:
    def __init__(self, time: string):
        self.is_extra_time = "+" in time
        if self.is_extra_time:
            self.time = int(time.split("+")[0].strip())
            self.extra_time = int(time.split("+")[1])
        else:
            self.time = int(time)
            self.extra_time = 0

    def is_after(self, time):
        if self.time == time.time:
            return self.extra_time > time.extra_time
        return self.time > time.time


