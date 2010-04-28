#!/usr/bin/env python
# vim: et ts=4 sw=4


# inherit everything from rapidsms, as default
# (this is optional. you can provide your own.)
from rapidsms.djangoproject.settings import *


# then add your django settings:

DATABASE_ENGINE = "sqlite3"
DATABASE_NAME = "db.sqlite3"

INSTALLED_APPS = (
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.auth",

    "rapidsms",
    "rapidsms.contrib.ajax", 
    "rapidsms.contrib.httptester", 
    "rapidsms.contrib.handlers", 
    "rapidsms.contrib.echo",
    "rapidsms.contrib.locations",
    "rapidsms.contrib.messagelog",
    "rapidsms.contrib.messaging",
    "rapidsms.contrib.scheduler",

    # enable the django admin using a little shim app (which includes
    # the required urlpatterns)
    "rapidsms.contrib.djangoadmin",
    "django.contrib.admin",
    
    "mwana.apps.contactsplus",
    "mwana.apps.registration",
    "mwana.apps.agents",
    "mwana.apps.labresults",
    "mwana.apps.reminders",
    "mwana.apps.tracing",
    "mwana.apps.location_importer",
#    "mwana.apps.supply",
    "mwana.apps.help",
    
    "rapidsms.contrib.default",
)

ADMIN_MEDIA_PREFIX = '/admin-media/'

# TODO: make a better default response, include other apps, and maybe 
# this dynamic?
DEFAULT_RESPONSE = "Sorry we couldn't understand that.  Valid keywords are JOIN, REQUEST, STATUS, and GOT. Respond with any keyword for more information." 

INSTALLED_BACKENDS = {
    "message_tester" : {"ENGINE": "rapidsms.backends.bucket" } 
}

TABS = [
    ('rapidsms.views.dashboard', 'Dashboard'),
    ('rapidsms.contrib.httptester.views.generate_identity', 'Message Tester'),
    ('rapidsms.contrib.locations.views.dashboard', 'Map'),
    ('rapidsms.contrib.messagelog.views.message_log', 'Message Log'),
    ('rapidsms.contrib.messaging.views.messaging', 'Messaging'),
#    ('rapidsms.contrib.registration.views.registration', 'Registration'),
    ('rapidsms.contrib.scheduler.views.index', 'Event Scheduler'),
#    ('mwana.apps.supply.views.dashboard', 'Supplies'),
    ('mwana.apps.labresults.views.dashboard', 'Results160'),
]

# Override the default log settings
LOG_LEVEL   = "DEBUG"
LOG_FILE    = "/var/log/rapidsms/rapidsms.log"
LOG_FORMAT  = "[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s"
LOG_SIZE    = 1000000 # in bytes
LOG_BACKUPS = 256     # number of logs to keep around

# import local settings if we find them
try:
    from localsettings import *
except ImportError:
    pass
