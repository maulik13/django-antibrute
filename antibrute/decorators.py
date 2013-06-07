from functools import wraps
from .main import *


def antibrute_login(func):
    """
    Wrapper for login view. This will take care of all the checks and
    displaying lockout page
    """
    @wraps(func)
    def wrap_login(request, *args, **kwargs):
        # TODO: IP check goes here here
        username = ''
        if request.method == 'POST':
            username = request.POST.get(FORM_USER_FIELD, '')
        if username:
            remaining_sec = check_and_update_lock(username)
            if remaining_sec:
                return get_lockout_response(request, remaining_sec)

        # original view
        response = func(request, args, kwargs)

        # check the result
        if request.method == 'POST':
            success = (response.status_code and response.has_header('location')
                       and request.user.is_authenticated)
            # add attempt and lock if threshold is reached
            process_login_attempt(request, username, success)

        return response
    return wrap_login
