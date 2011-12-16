import sys
import unittest
from tornado import ioloop

class PuritanicalIOLoop(ioloop.IOLoop):
    """
    A loop that quits when it encounters an Exception.
    """
    def handle_callback_exception(self, callback):
        exc_type, exc_value, tb = sys.exc_info()
        raise exc_value

class PuritanicalTest(unittest.TestCase):
    def setUp(self):
        super(PuritanicalTest, self).setUp()

        # So any function that calls IOLoop.instance() gets the
        # PuritanicalIOLoop instead of the default loop.
        if not ioloop.IOLoop.initialized():
            loop = PuritanicalIOLoop()
            loop.install()
        else:
            loop = ioloop.IOLoop.instance()
            self.assert_(
                isinstance(loop, PuritanicalIOLoop),
                "Couldn't install PuritanicalIOLoop"
            )