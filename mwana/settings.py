# inherit everything from rapidsms, as default
# (this is optional. you can provide your own.)
from rapidsms.djangoproject.settings import *

# Zambia:
RESULTS160_SLUGS = {
    'CBA_SLUG': 'cba',
    'PATIENT_SLUG': 'patient',
    'CLINIC_WORKER_SLUG': 'worker',
    'DISTRICT_WORKER_SLUG': 'district',
    'PROVINCE_WORKER_SLUG': 'province',
    # location types:
    'CLINIC_SLUGS': ('urban_health_centre', '1st_level_hospital',
                    'rural_health_centre', 'health_post'),
    'ZONE_SLUGS': ('zone',),
    'DISTRICT_SLUGS': ('districts',), # XXX verify me
    'PROVINCE_SLUGS': ('provinces',), # XXX verify me
}

TIME_ZONE = 'Africa/Lusaka'

LANGUAGE_CODE = 'bem-zm'

LOCATION_CODE_CLASS = 'mwana.zambia.locations.LocationCode'

# then add your django settings:
SEND_LIVE_LABRESULTS = True
SEND_LIVE_BIRTH_REMINDERS = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mwana.middleware.LoginRequired',
)

INSTALLED_APPS = [
    "mwana.apps.broadcast",
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
    
    "mwana.apps.stringcleaning",
    "mwana.apps.contactsplus",
    "mwana.apps.registration",
    "mwana.apps.agents",
    "mwana.apps.labresults",
    "mwana.apps.reminders",
    "mwana.apps.location_importer",
#    "mwana.apps.supply",
    
    "mwana.apps.reports",
    "mwana.apps.alerts",
    "mwana.apps.training",
    "mwana.apps.help",
    
    "rapidsms.contrib.default",
]

# These apps should not be started by rapidsms in your tests
# However the models + bootstrap will still be available through
# django
TEST_EXCLUDED_APPS = (
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rapidsms",
    "rapidsms.contrib.ajax",
    "rapidsms.contrib.httptester",
    "rapidsms.contrib.scheduler",
)

ADMIN_MEDIA_PREFIX = '/admin-media/'

# TODO: make a better default response, include other apps, and maybe 
# this dynamic?
DEFAULT_RESPONSE = "Invalid Keyword. Valid keywords are JOIN, AGENT, CHECK, RESULT, SENT, ALL, CBA, BIRTH and CLINIC. Respond with any keyword or HELP for more information."

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
    ('mwana.apps.labresults.views.mwana_reports', 'Reports'),
    ('mwana.apps.alerts.views.mwana_alerts', 'Alerts'),
]

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.auth', 'django.core.context_processors.debug', 'django.core.context_processors.i18n', 'django.core.context_processors.media', 'django.core.context_processors.request')
