#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import re
import datetime

from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.contrib.locations.models import Location, LocationType
from rapidsms.models import Contact

from mwana.apps.contactsplus.models import ContactType
from mwana.apps.tracing import models as tracing
from mwana.apps.reminders.tasks import send_appointment_reminder
from mwana import const


class TraceHelper(KeywordHandler):
    """
    """

    keyword = "trace"

    PATTERN = re.compile(r"^\s*(?P<patient>.+?)(:?\s+ZONE\s+(?P<zone>\w+))?$",
                         re.IGNORECASE)
    HELP_TEXT = "To trace a patient, send TRACE <PATIENT NAME> ZONE <ZONE>. "\
                "The zone is optional and the notification will be sent to "\
                "all CBAs for this clinic if it is left out."
    
    def help(self):
        self.respond(self.HELP_TEXT)

    def _send_trace(self, trace):
        pass
    
    def handle(self, text):
        if self.msg.contact is None or self.msg.contact.location is None or\
           not self.msg.contact.types.filter(slug=
                                             const.CLINIC_WORKER_SLUG).count():
            self.respond("Sorry, you must join as a clinic worker before you "
                         "can trace patents.")
            return
        m = self.PATTERN.search(text)
        if m is not None:
            patient_name = m.group('patient').strip()
            zone_slug = (m.group('zone') or '').strip()
            if zone_slug:
                zone_t, _ = LocationType.objects.get_or_create(slug='zone')
                try:
                    # TODO: also filter on parent clinic?
                    location = Location.objects.get(slug__iexact=zone_slug,
                                                    type=zone_t)
                except Location.DoesNotExist:
                    self.respond("Sorry, I don't know about a zone with code "
                                 "%(code)s. Please check your code and try again.",
                                 code=zone_slug)
            else:
                location = self.msg.contact.location
            patient_t = const.get_patient_type()
            try:
                patient = location.contact_set.get(name__iexact=patient_name,
                                                types__slug=const.PATIENT_SLUG)
                created = False
            except Contact.DoesNotExist:
                patient = location.contact_set.create(name=patient_name)
                patient.types.add(patient_t)
                created = True
            if created or not patient.types.filter(pk=patient_t.pk).count():
                patient.types.add(patient_t)
            try:
                trace = tracing.Trace.objects.get(patient=patient,
                                                date=datetime.datetime.today())
            except tracing.Trace.DoesNotExist:
                trace = None
            if trace:
                if trace.worker == self.msg.contact:
                    worker_name = 'you have'
                else:
                    worker_name = '%s has' % trace.worker.name
                self.respond("Sorry, %s(worker_name)s already "
                             "entered a trace request for %(name)s today. I "
                             "have notified the responsible CBAs and they "
                             "should be contacting the patient shortly.",
                             name=patient.name, worker_name=worker_name)
                return
            trace = tracing.Trace.objects.create(patient=patient,
                                                worker=self.msg.contact,
                                                date=datetime.datetime.today())
            connections = send_appointment_reminder(patient)
           # if connections:
            self.respond("Thank you %(worker)s. I have sent a message to "
                         "the responsible RemindMi agents to trace "
                         "%(patient)s and tell him or her to come to the "
                         "clinic.", worker=self.msg.contact.name,
                         patient=patient.name)
#            else:
#                self.respond("I'm sorry, %(worker)s. I couldn't find any "
#                             "RemindMi agents to trace %(patient)s.",
#                             worker=self.msg.contact.name,
#                             patient=patient.name)
        else:
            self.respond("Sorry, I didn't understand that. Make sure you send "
                         "your patient name and zone like: TRACE <PATIENT> "
                         "ZONE <ZONE>")
