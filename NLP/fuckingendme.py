import spacy
from datetime import datetime
from spacy.symbols import prep
from autocorrect import Speller
import re

nlp = spacy.load('en_core_web_lg')

doc = nlp("I want a ticket on the 15th from Norwich to Cambridge arriving at 13:00 and i want a return ticket for the 18th leaving at 14:00")

for ent in doc.ents:
    print(ent.text, ent.label_)