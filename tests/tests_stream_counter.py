import unittest
import sys
from datetime import datetime
from stream_counter import stream_counter


class tests_stream_counter(unittest.TestCase):
    def test__renew__whenCalledWithFourSequentialRequests__returnsTrueForTheFirstThreeAndFalseForTheFourth(self):
        sc = stream_counter()

        self.assertEqual(sc.renew('S00', 90, 3), True)
        self.assertEqual(sc.renew('S01', 90, 3), True)
        self.assertEqual(sc.renew('S02', 90, 3), True)
        self.assertEqual(sc.renew('S03', 90, 3), False)

        print(sys.getsizeof(sc))

    def test__renew__whenCalledWithSuccessiveSequentialRequestsButZeroRenewalTime__alwaysReturnsTrue(self):
        sc = stream_counter()

        for i in range(0, 1000):
            self.assertEqual(sc.renew('S%i' % i, 0, 3), True)

        print(sys.getsizeof(sc))

    def test__renew__timing__whenCalledWithOneHundredThousandSequentialRequests__recordsTimeTaken(self):
        sc = stream_counter()

        start_time = datetime.utcnow()

        for i in range(0, 100000):
            sc.renew('S%i' % i, 0, 3)

        print('100k renews completed in time %s' % (datetime.utcnow() - start_time))
        print(sys.getsizeof(sc))
