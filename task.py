"""Created by Nolan Jessen for CPR E 558 on 10/20/2020"""

class Task:
    """This class simulates a single Task to be used for analyzing.

    This class contains two values, runtime and deadline, that can be used for analyzing
    the individual Task, comparing with other Tasks, and eventually creating a schedule
    out of.
    """
    def __init__(self, runtime, deadline, minruntime, minpercent):
        self.runtime = runtime
        self.deadline = deadline
        self.minruntime = minruntime
        self.minpercent = minpercent

    def getString(self):
        s = "{}{}{}{}".format(" Runtime: ", self.runtime, " Deadline: ", self.deadline)
        return s