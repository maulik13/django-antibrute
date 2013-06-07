from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.db import backend
from django.db.models import Sum

from .appsettings import (RECENT_INTERVAL_SEC, DIST_FAST_INTERVAL_SEC,
                          LOCKOUT_COUNT_LIMIT)
from .utils import *


class AccessAttemptManager(models.Manager):

    def get_latest_attempt(self, request, username):
        params = get_info_from_request(request)
        params['username'] = username
        last_attempt = self.filter(**params).latest('attempted_at')
        return last_attempt

    def add_attempt(self, request, username, safe=False):
        """
        If the attempt was safe (success) then add as a new entry
        If not safe then get the last attempt
        If the last attempt is safe then add failed as new entry
        If the last attempt is not safe and is recent add to count
        """
        create_new = True
        if not safe:
            try:
                last_attempt = self.get_latest_attempt(request, username)
                if last_attempt.was_recent() and not last_attempt.safe:
                    last_attempt.attempted_at = timezone.now()
                    last_attempt.count += 1
                    last_attempt.save()
                    create_new = False
            except AccessAttempt.DoesNotExist:
                pass
        if create_new:
            params = get_info_from_request(request)
            params['safe'] = safe
            params['username'] = username
            last_attempt = self.model(**params)
            last_attempt.save()
        return last_attempt

    def get_attempt_status(self, request, username):
        """
        Returns severity based on count,
        -2 no attempt logged
        -1 success is logged
        0 means logged failure but safe
        """
        try:
            last_attempt = self.get_latest_attempt(request, username)
            if not last_attempt.safe:
                return last_attempt.get_severity()
            else:
                return -1
        except AccessAttempt.DoesNotExist:
            return -2

    def get_lastest_user_status(self, username):
        """
        Get the given user's latest status
        """
        try:
            attempt = self.filter(username=username).latest('attempted_at')
            return attempt.get_severity()
        except AccessAttempt.DoesNotExist:
            return -1

    def get_recent_user_attempts(self, username):
        """
        """
        oldest_time = timezone.now() - timedelta(seconds=DIST_FAST_INTERVAL_SEC)
        attempts = self.filter(username=username, attempted_at__gt=oldest_time)
        return attempts

    def get_recent_user_failed_attempts(self, username):
        """
        """
        oldest_time = timezone.now() - timedelta(seconds=DIST_FAST_INTERVAL_SEC)
        attempts = self.filter(username=username, attempted_at__gt=oldest_time) \
            .extra(where=["id > (SELECT max(id) from {0} WHERE username=%s AND safe=TRUE)".format(self.model._meta.db_table)], params=[username]) \
            .values('id', 'ip_address', 'attempts', 'attempted_at')
        return attempts

    def get_recent_fails_for_user(self, username):
        """
        """
        oldest_time = timezone.now() - timedelta(seconds=DIST_FAST_INTERVAL_SEC)
        access_attempts = self.filter(username=username, attempted_at__gt=oldest_time)
        fail_count = 0
        total = len(access_attempts)
        for i in range(0, total):
            if access_attempts[i].safe:
                break
            fail_count += access_attempts[i].count
        return fail_count
#        oldest_time = timezone.now() - timedelta(seconds=DIST_FAST_INTERVAL_SEC)
#        total_aggr = self.filter(username=username, attempted_at__gt=oldest_time) \
#                            .extra(where=["id > (SELECT max(id) from {0} WHERE username=%s AND safe=TRUE)".format(self.model._meta.db_table)],params=[username]) \
#                            .aggregate(failed_attempts=Sum('attempts'))
#        return total_aggr['failed_attempts']

    def get_recent_fails_for_ip(self, ip_address):
        """
        """
        oldest_time = timezone.now() - timedelta(seconds=DIST_FAST_INTERVAL_SEC)
        total_aggr = self.filter(ip_address=ip_address, attempted_at__gt=oldest_time) \
            .extra(where=["id > (SELECT max(id) from {0} WHERE ip_address=%s AND safe=TRUE)".format(self.model._meta.db_table)], params=[ip_address]) \
            .aggregate(failed_attempts=Sum('count'))
        return total_aggr['failed_attempts']


class AccessAttempt(models.Model):
    """
    Model for storing attempts on forms
    """
    ip_address = models.IPAddressField('IP address',
                                       null=True)
    user_agent = models.CharField(max_length=255,
                                  null=True,
                                  blank=True)
    # e.g. store field values or any other info here
    username = models.CharField(max_length=255,
                                default='',
                                blank=True)
    safe = models.BooleanField(default=False)
    count = models.IntegerField(default=1)
    attempted_at = models.DateTimeField(default=timezone.now, db_index=True)

    objects = AccessAttemptManager()

    class Meta:
        ordering = ['-attempted_at']

    def __unicode__(self):
        return u"{0}:{1} Attempt from : {2} at {3} for {4}".format(
            self.safe, self.count, self.ip_address, self.attempted_at, self.username)

    def was_recent(self):
        return timezone.now() - self.attempted_at < timedelta(seconds=RECENT_INTERVAL_SEC)

    def get_severity(self):
        if self.count > FAILURE_COUNT_LEVEL1:
            return 1
        return 0


class LockedUser(models.Model):
    """
    """
    username = models.CharField(max_length=255, unique=True, db_index=True)
    locked_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return u'{0} locked at {1}'.format(self.username, self.locked_at)


class LockedIP(models.Model):
    ip_address = models.ForeignKey(AccessAttempt)
    locked_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return u'{0} locked at {1}'.format(self.ip_address, self.locked_at)
