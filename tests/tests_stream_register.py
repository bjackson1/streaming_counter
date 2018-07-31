import unittest
import sys
from datetime import datetime
from stream_register import stream_register


class tests_stream_register(unittest.TestCase):
    def test__renew__whenCalledWithFourSequentialRequestsForDifferingSubscribers__returnsTrueForAll(self):
        sr = stream_register()

        self.assertEqual(sr.renew('sub00', 'str00'), True)
        self.assertEqual(sr.renew('sub01', 'str01'), True)
        self.assertEqual(sr.renew('sub02', 'str02'), True)
        self.assertEqual(sr.renew('sub03', 'str03'), True)

    def test__renew__whenCalledWithFourSequentialRequestsForASingleSubscriber__returnsTrueForTheFirstThreeThenFalse(self):
        sr = stream_register()

        self.assertEqual(sr.renew('sub00', 'str00'), True)
        self.assertEqual(sr.renew('sub00', 'str01'), True)
        self.assertEqual(sr.renew('sub00', 'str02'), True)
        self.assertEqual(sr.renew('sub00', 'str03'), False)

    def test__renew__whenCalledWithOneHundredThousandDifferingSubscribers__returnsTrueForAll(self):
        sr = stream_register()

        for i in range(0, 100000):
            self.assertEqual(sr.renew('sub%s' % i, 'str00'), True)

    def test__renew__whenCalledWithOneHundredThousandDifferingSubscribersAndFourStreamsEach__returnsTrueForAllFirstThreeThenFalseForLast(self):
        sr = stream_register()

        for i in range(0, 100000):
            self.assertEqual(sr.renew('sub%s' % i, 'str00'), True)
            self.assertEqual(sr.renew('sub%s' % i, 'str01'), True)
            self.assertEqual(sr.renew('sub%s' % i, 'str02'), True)
            self.assertEqual(sr.renew('sub%s' % i, 'str03'), False)

