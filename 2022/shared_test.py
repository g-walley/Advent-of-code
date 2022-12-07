import time
import unittest


class AOCTest(unittest.TestCase):
    def setUp(self) -> None:
        self.start_time = time.time()

    def tearDown(self) -> None:
        t = time.time() - self.start_time
        time.sleep(0.1)
        if 0.001 <= t < 1:
            print('%s: %.3fms' % (self.id(), t*1000))
        elif 0.000001 <= t < 0.001:
            print('%s: %.3fus' % (self.id(), t*1000000))
        elif t < 0.000001:
            print('<1us')
        else:
            print('%s: %.3fs' % (self.id(), t))
        time.sleep(0.1)
