from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import AccessAttempt, LockedUser
from .appsettings import (LOCKOUT_COUNT_LIMIT, COOLOFF_PERIOD_SEC,
                          LOCKOUT_TEMPLATE, LOCKOUT_MSG_URL)


lockout_msg = "Too many login attempts. Please try again in few seconds."


def process_login_attempt(request, username, success):
    """
    """
    attempt = AccessAttempt.objects.add_attempt(request, username, safe=success)
    # if failed find the count and update lock status
    if not success:
        failed_attempts = AccessAttempt.objects.get_recent_fails_for_user(username)
        if failed_attempts >= LOCKOUT_COUNT_LIMIT:
            lock_user(username)


def lock_user(username):
    user_entry, is_exist = LockedUser.objects.get_or_create(username=username)
    if is_exist:
        user_entry.locked_at = timezone.now()
        user_entry.save()
    return user_entry


def check_and_update_lock(username):
    """
    Check lock status, if expired then delete
    """
    try:
        locked_user_status = LockedUser.objects.get(username=username)
        time_since_locked = timezone.now() - locked_user_status.locked_at
        remaining_sec = COOLOFF_PERIOD_SEC - time_since_locked.total_seconds()
        if remaining_sec > 0:
            return remaining_sec
        else:
            locked_user_status.delete()
    except LockedUser.DoesNotExist:
        pass
    return None


def get_lockout_response(request, remaining_sec):
    if LOCKOUT_MSG_URL:
        return redirect(LOCKOUT_MSG_URL)

    if LOCKOUT_TEMPLATE:
        context = {'time_remaining': remaining_sec}
        return render(request, LOCKOUT_TEMPLATE, context)

    return HttpResponse(lockout_msg)
