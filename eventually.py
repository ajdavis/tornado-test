import os
import time
import unittest

from tornado import ioloop

class AssertEventuallyTest(unittest.TestCase):
    def setUp(self):
        super(AssertEventuallyTest, self).setUp()

        # Callbacks registered with assertEventuallyEqual()
        self.assert_callbacks = set()

    def assertEventuallyEqual(
            self, expected, fn, msg=None, timeout_sec=None
    ):
        if timeout_sec is None:
            timeout_sec = 5
        timeout_sec = max(timeout_sec, int(os.environ.get('TIMEOUT_SEC', 0)))
        start = time.time()
        loop = ioloop.IOLoop.instance()

        def callback():
            try:
                self.assertEqual(expected, fn(), msg)
                # Passed
                self.assert_callbacks.remove(callback)
                if not self.assert_callbacks:
                    # All asserts have passed
                    loop.stop()
            except AssertionError:
                # Failed -- keep waiting?
                if time.time() - start < timeout_sec:
                    # Try again in about 0.1 seconds
                    loop.add_timeout(time.time() + 0.1, callback)
                else:
                    # Timeout expired without passing test
                    loop.stop()
                    raise

        self.assert_callbacks.add(callback)

        # Run this callback on the next I/O loop iteration
        loop.add_callback(callback)
