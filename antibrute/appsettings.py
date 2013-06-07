from django.conf import settings

app_prefix = 'ANTIBRUTE_'


# user field exptected in POST
FORM_USER_FIELD = getattr(settings, app_prefix + 'FORM_USER_FIELD', 'username')

# Thresholds before action is required
LOCKOUT_COUNT_LIMIT = getattr(settings, app_prefix + 'LOCKOUT_COUNT_LIMIT', 10)

# if attempt is within this interval then it is recent
RECENT_INTERVAL_SEC = getattr(settings, app_prefix + 'RECENT_INTERVAL_SEC', 15)

# Interval indicating attempt was recent (for distributed attack)
DIST_FAST_INTERVAL_SEC = getattr(settings, app_prefix + 'DIST_FAST_INTERVAL_SEC', 15)

COOLOFF_PERIOD_SEC = getattr(settings, app_prefix + 'COOLOFF_PERIOD_SEC', 15)

LOCKOUT_MSG_URL = getattr(settings, app_prefix + 'LOCKOUT_MSG_URL', '')

LOCKOUT_TEMPLATE = getattr(settings, app_prefix + 'LOCKOUT_TEMPLATE', '')
