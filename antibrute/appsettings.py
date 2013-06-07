from django.conf import settings

app_prefix = 'ANTIBRUTE_'


# user field exptected in POST for authenticating a user
FORM_USER_FIELD = getattr(settings, app_prefix + 'FORM_USER_FIELD', 'username')

# Number of failed attempts before a user name is marked locked
LOCKOUT_COUNT_LIMIT = getattr(settings, app_prefix + 'LOCKOUT_COUNT_LIMIT', 10)

# If attempt is within this interval then it is recent
RECENT_INTERVAL_SEC = getattr(settings, app_prefix + 'RECENT_INTERVAL_SEC', 15)

# Interval indicating an attempt was recent for distributed fast attack
DIST_FAST_INTERVAL_SEC = getattr(settings, app_prefix + 'DIST_FAST_INTERVAL_SEC', 15)

# Duration for keeping a user name locked
COOLOFF_PERIOD_SEC = getattr(settings, app_prefix + 'COOLOFF_PERIOD_SEC', 15)

# If you want to redirect to a specific page when locked out use this variable
LOCKOUT_MSG_URL = getattr(settings, app_prefix + 'LOCKOUT_MSG_URL', '')

# Use this template to render lockout message
LOCKOUT_TEMPLATE = getattr(settings, app_prefix + 'LOCKOUT_TEMPLATE', '')
