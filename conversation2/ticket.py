from experta import *
from datetime import datetime

from tickets.scraping import find_cheapest_ticket

from .facts import *


class TicketRules:
    # Ready to get ticekt
    @Rule(
        DepartingFrom(MATCH.dep_from)
        & DepartingTo(MATCH.dep_to)
        & DepartureTime(date=MATCH.date, time=MATCH.time)
        & Returning(MATCH.ret))
    def find_ticket(self, dep_from, dep_to, date, time, ret):
        self.output_statement("BOT:\tFinding your ticket now.")

        # For testing purposes, it's automatically in 2019.
        # Some other things are being assumed as well
        departure_date = datetime.strptime('{}/19 {}'.format(date, time),
                                           '%d/%m/%y %H:%M')
        ticket = find_cheapest_ticket(dep_from, dep_to, {
            'condition': 'dep',
            'date': departure_date
        })

        # Eventually, we output this properly
        self.output_statement('BOT:\t' + str(ticket))
