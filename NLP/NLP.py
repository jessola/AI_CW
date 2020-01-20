import spacy
from datetime import datetime
from spacy.symbols import prep

nlp = spacy.load('en_core_web_lg')

#input = "I want a ticket from norwich to ely at 2:00pm on the 17th and return on the 18th and get there by 6:00pm"
def inputNLP(input, returningInput = None):

    doc = nlp(input)
    returning = None
    returnToken = None
    ticketdict = {
        "departing_from": None,
        "departing_to": None,
        "departure_condition": None,
        "departure_date": None,
        "departure_time": None,
        "num_adults": None,
        "num_children": None,
        "returning": returningInput,
        "return_condition": None,
        "return_date": None,
        "return_time" : None  
    }

    """for ent in doc.ents:
        print(ent.text, ent.label_)"""
    #find if returning
    for token in doc:
        if token.lemma_ == "return":
            returning = True
            tokenReturning = token.i
            ticketdict.update({"returning": True})

    #print(returning)
    #print(tokenReturning)

    for ent in doc.ents:

        
        if (returning == True and ent.start < tokenReturning) or (returningInput == True) or (returning != True and returningInput != True) :
            if ent.label_ == "GPE":
                if ent.start != 0:
                    prev_token = doc[ent.start - 1]
                    if prev_token.text in ("From", "from"):
                        ticketdict.update({"departing_from": ent.text})
                    if prev_token.text in ("to"):
                        ticketdict.update({"departing_to": ent.text})

            #find departure date
            if ent.label_ == "DATE":
                date = ent.text_
                date = re.sub("[^0-9]", '', date)
                datenew = datetime.now()
                depdate = datenew.replace(day = int(date), hour = 0, minute = 0, second = 0).strftime('%d%m%y')
                ticketdict.update({"return_date": depdate})

            #find departure condition or time
            if ent.label_ == "TIME":
                if ent.start != 0: 
                    prev_token1 = doc[ent.start - 1]
                    prev_token2 = doc[ent.start - 2]
                    if  prev_token1.dep == prep and prev_token2.lemma_ in ("arrive", "there"):
                        ticketdict.update({"departure_condition": "arr"})
                        strtime = ent.text
                        in_time = datetime.strptime(strtime, "%I:%M%p")
                        out_time = datetime.strftime(in_time, "%H%M")
                        ticketdict.update({"departure_time": out_time})
                    else:
                        ticketdict.update({"departure_condition": "dep"})  
                        strtime = ent.text
                        in_time = datetime.strptime(strtime, "%I:%M%p")
                        out_time = datetime.strftime(in_time, "%H%M")
                        ticketdict.update({"departure_time": out_time})

        #find num_adults
        if ent.label_ == "CARDINAL" and ent.start != len(doc) - 1:
            next_token = doc[ent.start + 1]
            if  next_token.lemma_ in ("adult"):
                ticketdict.update({"num_adults": ent.text})
        #find num_children
        if ent.label_ == "CARDINAL" and ent.start != len(doc) - 1:
            next_token = doc[ent.start + 1]
            if  next_token.lemma_ in ("child", "kid"):
                ticketdict.update({"num_children": ent.text})

        if (returning == True and ent.start > tokenReturning) or returningInput == True:

            #find return date
            if ent.label_ == "DATE":
                date = ent.text_
                date = re.sub("[^0-9]", '', date)
                datenew = datetime.now()
                depdate = datenew.replace(day = int(date), hour = 0, minute = 0, second = 0).strftime('%d%m%y')
                ticketdict.update({"return_date": depdate})

            #find return condition or time
            if ent.label_ == "TIME":
                if ent.start != 0: 
                    prev_token1 = doc[ent.start - 1]
                    prev_token2 = doc[ent.start - 2]
                    if  prev_token1.dep_ == "prep" and (prev_token2.lemma_ in ("arrive", "there")):
                        ticketdict.update({"return_condition": "arr"})
                        strtime = ent.text
                        in_time = datetime.strptime(strtime, "%I:%M%p")
                        out_time = datetime.strftime(in_time, "%H%M")
                        ticketdict.update({"departure_time": out_time})
                    else:
                        ticketdict.update({"return_condition": "dep"})  
                        strtime = ent.text
                        in_time = datetime.strptime(strtime, "%I:%M%p")
                        out_time = datetime.strftime(in_time, "%H%M")
                        ticketdict.update({"departure_time": out_time})

    return ticketdict

print(inputNLP("I want a ticket from norwich to ely at 2:00pm on the 17th and return on the 18th and get there by 6:00pm"))
