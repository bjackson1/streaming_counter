import unittest
import mock
import frontedge
import json


class tests_frontedge(unittest.TestCase):
    def setUp(self):
        self.app = frontedge.app.test_client()

    def test__renew__whenCalledWithSingleRenewRequest__returnsStatusOK(self):
        web_resp = self.app.get('/renew/sub00/str00')
        self.assertEqual(200, web_resp.status_code)
        resp = json.loads(web_resp.data.decode(web_resp.charset))

        self.assertIn('status', resp)
        self.assertEqual(resp['status'], 'OK')

    def test__renew__whenCalledWithFourRenewRequestsForTheSameSubscriber__returnsStatusOKForTheFirstThreeAndStatusSubscriptionLimitReachedForTheFourth(self):
        for i in range(0, 3):
            web_resp = self.app.get('/renew/sub01/str%s' % i)
            resp = json.loads(web_resp.data.decode(web_resp.charset))

            self.assertIn('status', resp)
            self.assertEqual(resp['status'], 'OK')

        web_resp = self.app.get('/renew/sub01/str03')
        resp = json.loads(web_resp.data.decode(web_resp.charset))

        self.assertIn('status', resp)
        self.assertEqual(resp['status'], 'SubscriptionLimitReached')

    def test__renew__whenCalledAndRequestFailedWithExceptionOnRenewal__returnsStatusRequestFailed(self):
        with mock.patch('stream_register.stream_register.renew', side_effect=Exception):
            web_resp = self.app.get('/renew/sub02/str00')
            self.assertEqual(500, web_resp.status_code)
            resp = json.loads(web_resp.data.decode(web_resp.charset))

            self.assertIn('status', resp)
            self.assertEqual(resp['status'], 'RequestFailed')
