#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from mwana.apps.stringcleaning.inputcleaner import InputCleaner
from rapidsms.contrib.handlers import KeywordHandler

UNGREGISTERED = "Sorry, you must be registered with Results160 to report DBS samples sent. If you think this message is a mistake, respond with keyword 'HELP'"
SENT          = "Hello %(name)s! We received your notification that %(count)s DBS samples were sent to us today from %(clinic)s. We will notify you when the results are ready."
HELP          = "To report DBS samples sent, send SENT <NUMBER OF SAMPLES>"
SORRY         = "Sorry, we didn't understand that message."

class SentHandler(KeywordHandler):
    """
    """

    keyword = "sent|send|sen|snt|cent"

    def help(self):
        self.respond(HELP)

    def handle(self, text):
        if not self.msg.contact:
            self.respond(UNGREGISTERED)
            return
        b = InputCleaner()
        try:
            count = int(b.try_replace_oil_with_011(text.strip()))
        except ValueError:
            text = b.words_to_digits(text)
            if not text:
                self.respond("%s %s" % (SORRY, HELP))
                return
            else:
                count = int(text)
            
        if count < 1:
            self.respond("Sorry, the number of DBS samples sent must be greater than 0 (zero).")
            return

        # TODO: maybe record this somewhere
        self.respond(SENT, name=self.msg.contact.name, count=count,
                     clinic=self.msg.contact.location)
                     
        