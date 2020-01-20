import spacy

nlp = spacy.load('en_core_web_lg')

doc = nlp("I want a ticket from norwich to ely at 2:00pm on the 17th and return on the 18th and get there by 6:00pm ")

for ent in doc.ents:
    print(ent.text, ent.label_)