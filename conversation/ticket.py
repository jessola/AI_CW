from experta import *
from datetime import datetime

from tickets.scraping import find_cheapest_ticket


class TicketRules:
    # Ready to find ticket
    @Rule(
        AS.f1 << Fact(departing_from=MATCH.dep_from)
        & AS.f2 << Fact(departing_to=MATCH.dep_to)
        & Fact(departure_time=MATCH.dep_time)
        & Fact(departure_condition=MATCH.dep_condition)
        & Fact(returning=MATCH.returning)
        & (Fact(return_time=MATCH.ret_time) | AS.ret_time << Fact(return_time=~W()))
        # & (
        #     AS.returning << Fact(returning=True) & Fact(return_time=MATCH.ret_time)
        #     | AS.returning << Fact(returning=False) & ~Fact(return_time=MATCH.ret_time)
        # )
    )
    def find_ticket(
        self, f1, f2, dep_from, dep_to, dep_time, dep_condition, returning, ret_time
    ):
        try:
            print(
                find_cheapest_ticket(
                    dep_from,
                    dep_to,
                    {"condition": dep_condition, "date": dep_time},
                    {"condition": "dep", "date": ret_time} if returning else None,
                )
            )
        except:
            print("There are no tickets available based on your specifications")

            # Get rid of some facts (Handle this with rules later)
            self.retract(f1)
            self.remaining_questions.append("departing_from")

            self.retract(f2)
            self.remaining_questions.append("departing_to")
