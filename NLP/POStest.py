import spacy

nlp = spacy.load('en_core_web_sm')

doc = nlp("An apple a day")

for token in doc:
    print(token.text, token.label_)