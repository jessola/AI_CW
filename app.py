from durable.lang import assert_fact

# from animal import initialise_animal_rules
from questions_asked import init_questions_answered
from questions import ask_question


def main():
    init_questions_answered()
    # print("FROM:\t", ask_question("departing_from"))
    # print("TO:\t", ask_question("departing_to"))
    # print("ADULTS:\t", ask_question("num_adults"))
    # print("CHILD:\t", ask_question("num_children"))
    # print("TIME:\t", ask_question("departure_time"))
    question = assert_fact("questions_answered", {"type": "departing_from"})
    question = assert_fact("questions_answered", {"type": "departing_from"})


if __name__ == "__main__":
    main()

