"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


from django.utils import unittest
from django.test.client import RequestFactory
from django.conf import settings

import appsettings
from .main import *
from .models import AccessAttempt, LockedUser


class AntiBruteTest(unittest.TestCase):

    def setUp(self):
        appsettings.LOCKOUT_MSG_URL = ''
        appsettings.LOCKOUT_TEMPLATE = ''

        self.reqeust_factory = RequestFactory()
        self.test_username = 'any_random_user'
        AccessAttempt.objects.all().delete()
        LockedUser.objects.all().delete()

    def _create_attempts(self, username, number, success=False):
        # just for creating request, we don't actually use login view
        request = self.reqeust_factory.get(settings.LOGIN_URL)
        for i in range(0, number):
            process_login_attempt(request, username, success)

    def test_failed_attempts_addup(self):
        request = self.reqeust_factory.get(settings.LOGIN_URL)
        self._create_attempts(self.test_username, appsettings.LOCKOUT_COUNT_LIMIT - 1)
        # number of attempts should be added up
        last_access = AccessAttempt.objects.get_latest_attempt(request, self.test_username)
        self.assertEqual(last_access.count, appsettings.LOCKOUT_COUNT_LIMIT - 1)

    def test_user_lockup(self):
        # just for creating request, we don't actually use login view
        self._create_attempts(self.test_username, appsettings.LOCKOUT_COUNT_LIMIT - 1)
        # still not locked
        locked_user_qs = LockedUser.objects.filter(username=self.test_username)
        self.assertFalse(locked_user_qs.exists())
        # add one more attempt
        self._create_attempts(self.test_username, 1)
        # now should be locked
        locked_user_qs = LockedUser.objects.filter(username=self.test_username)
        self.assertEqual(len(locked_user_qs), 1)

    def test_lockup_after_success(self):
        # just for creating request, we don't actually use login view
        self._create_attempts(self.test_username, appsettings.LOCKOUT_COUNT_LIMIT - 1)
        self._create_attempts(self.test_username, 1, True)
        self._create_attempts(self.test_username, appsettings.LOCKOUT_COUNT_LIMIT - 1)
        # Also there should be total three entries right now
        self.assertEqual(AccessAttempt.objects.all().count(), 3)
        # shuold still not be locked
        locked_user_qs = LockedUser.objects.filter(username=self.test_username)
        self.assertFalse(locked_user_qs.exists())
