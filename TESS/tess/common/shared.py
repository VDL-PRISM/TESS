from functools import wraps
import time
import logging
import logging.config

LOGGER = logging.getLogger()

class throttle(object):
    """ Throttle a function to execute at most X time per <seconds> seconds
        The function is executed on the forward edge.
    """
    def __init__(self, limit, seconds):
        self.limit = limit
        self.seconds = seconds
        self.count = 0
        self.first_run = None

    def __call__(self, fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            if self.first_run is None:
                self.first_run = time.time()

            now = time.time()
            LOGGER.debug("%s > %s", now, (self.first_run + self.seconds))
            if now > self.first_run + self.seconds:
                # Enough time as elapsed that the count can be reset
                LOGGER.debug("Setting count to zero")
                self.count = 0
                self.first_run = now

            if self.count >= self.limit:
                LOGGER.debug("Over limit!")
                return

            self.count += 1
            fn(*args, **kwargs)

        return wrap


class DatabaseException(Exception):
    pass


class StateUpdateException(Exception):
    pass


class NotificationException(Exception):
    pass


class EcobeeState:
    def run(self):
        assert 0, "run not implemented"

    def next(self, input):
        assert 0, "next not implemented"

    def check(self):
        assert 0, "update state not implemented"
