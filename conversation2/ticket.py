from experta import *

from .facts import *


class TicketRules:
    # Ready to get ticekt
    @Rule(
        DepartingFrom(MATCH.dep_from)
        & DepartingTo(MATCH.dep_to)
        & DepartureTime(date=MATCH.date, time=MATCH.time)
        & Returning(MATCH.ret)
    )
    def find_ticket(self, dep_from, dep_to, date, time, ret):
        self.output_statement("BOT:\tFinding your ticket now.")
