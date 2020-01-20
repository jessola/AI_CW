import spacy
from datetime import datetime
import re

#nlp = spacy.load('en_core_web_lg')

#doc = nlp("I want a ticket from norwich to ely at 2:00pm on the 17th and return on the 18th and get there by 6:00pm ")

#for ent in doc.ents:
#    print(ent.text, ent.label_)

#depdate = date.today()

date = "the 17th"
date = re.sub("[^0-9]", '', date)
datenew = datetime.now()
depdate = datenew.replace(day = int(date), hour = 0, minute = 0, second = 0).strftime('%d%m%y')
print(depdate)



