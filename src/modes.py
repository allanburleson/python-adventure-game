import threading
import time


# Note: this may do something later in life.
threads = []


class Mode(object):
    """Documentation for Mode:
        - A mode is able to run in the background.
        - However, it does not have to.
    """

    def __init__(self, name):
        self.name = name

    def async_start(self, func):
        t = threading.Thread(target=func)
        threads.append(t)
        t.start()


# Some helpful modes.
class Timer(Mode):
    """Documentation for Timer:
        Create an instance of a timer.
        A timer has:
            1. An amount to count down (amount)
            2. How long to wait between each count (wait_for)

    """

    def __init__(self, amount, wait_for):
        super(Timer, self).__init__("timer")
        self.amount = amount
        self.wait_for = wait_for

    def timer(self):
        amount = self.amount
        while amount != -1:
            amount = amount - 1
            time.sleep(self.wait_for)


class Cutscene(Mode):
    """Documentation for Cutscene

    """

    def __init__(self, description, scroll=0):
        super(Cutscene, self).__init__("cutscene")
        assert type(description) == list
        self.description = description
        self.scroll = scroll

    def cutscene(self):
        if self.scroll == 0:
            print(self.description[0])
            input(">>")
        else:
            i = 0
            while i < len(self.description):
                print(self.description[i])
                input(">>")
                i += 1
