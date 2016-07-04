import threading

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

    def __init__(self, time):
        super(Timer, self).__init__("timer", 1)
        self.time = time

    def timer(self):
        time = self.time
        while time != -1:
            print("FOOBAR")
            time = time - 1

    def pStart(self):
        t = threading.Thread(target=self.timer)
        threads.append(t)
        t.start()


timer = Timer(500)
timer.pStart()


# t = threading.Thread(target=timer.timer)
# t.start()
