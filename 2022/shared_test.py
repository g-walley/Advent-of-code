import time
import unittest


class AOCTest(unittest.TestCase):
    def setUp(self) -> None:
        self.startTime = time.time()

    def tearDown(self) -> None:
        t = time.time() - self.startTime
        if 0.001 <= t < 1:
            print('%s: %.3fms' % (self.id(), t*1000))
        elif 0.0000001 <= t < 0.001:
            print('%s: %.3fus' % (self.id(), t*1000000))
        else:
            print('%s: %.3f' % (self.id(), t*1000))
