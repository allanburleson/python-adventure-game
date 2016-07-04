import threading
import time


# Note: this may do something later in life.
threads = []


class Mode(object):
    """Documentation for Mode
        So the mode class _still_ doesn't do anything.
        I'd really like for the async_start function to
        put the current function in the background

        Example:
        ```
        def afunction(self):
            Mode.async_start()  # Background process
            # Whatever else
        ```
    """

    def __init__(self, name, async):
        self.name = name
        self.async = async

    # def async_start(self):


class Timer(Mode):
    """Documentation for Timer

    """

    def __init__(self, amount):
        super(Timer, self).__init__("timer", 1)
        self.amount = amount

    def timer(self):
        amount = self.amount
        while amount != -1:
            print("FOOBAR")
            amount = amount - 1
            time.sleep(10)

    def pStart(self):
        t = threading.Thread(target=self.timer)
        threads.append(t)
        t.start()


timer = Timer(500)
timer.pStart()


# t = threading.Thread(target=timer.timer)
# t.start()
