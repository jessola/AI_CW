import spacy
from datetime import datetime
import re

nlp = spacy.load('en_core_web_lg')

doc = nlp("6pm, 6:00am, six pm, six o clock, 13:00 these are all time variants")

for ent in doc.ents:
  print(ent.text, ent.label_)

#depdate = date.today()

#date = "the 17th"
#date = re.sub("[^0-9]", '', date)
#datenew = datetime.now()
#depdate = datenew.replace(day = int(date), hour = 0, minute = 0, second = 0).strftime('%d%m%y')
#print(depdate)

'''for ent in doc.ents:
    if ent.label_ == "TIME":
                    if ent.start != 0: 
                        prev_token1 = doc[ent.start - 1]
                        prev_token2 = doc[ent.start - 2]
                        if  prev_token1.dep_ == "prep" and (prev_token2.lemma_ in ("arrive", "there")):
                            ticketdict.update({"return_condition": "arr"})
                            ticketdict.update({"return_time": timeFormat(ent.text)})
                        else:
                            ticketdict.update({"return_condition": "dep"})  
                            ticketdict.update({"return_time": timeFormat(ent.text)})'''



