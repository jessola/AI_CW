import spacy
from datetime import datetime
from spacy.symbols import prep
from autocorrect import Speller
import re

nlp = spacy.load('en_core_web_lg')

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

    #find if returning 
    for token in doc:
        #return tagger
        if token.lemma_ == "return":
            returning = True
            tokenReturning = token.i
            ticketdict.update({"returning": True})


    #using entity 
    for ent in doc.ents:

        #departures
        if (returning == True and ent.start < tokenReturning) or (returningInput == True) or (returning != True and returningInput != True) :
            if ent.label_ == "GPE":
                if ent.start != 0:
                    prev_token = doc[ent.start - 1]
                    if prev_token.lemma_ in ("from", "depart"):
                        ticketdict.update({"departing_from": ent.text})
                    if prev_token.lemma_ in ("to", "at"):
                        ticketdict.update({"departing_to": ent.text})

            #find departure date
            if ent.label_ == "DATE":
                ticketdict.update({"departure_date": dateFormat(ent.text)})

            #find departure condition or time
            if ent.label_ == "TIME":
                if ent.start != 0: 
                    prev_token1 = doc[ent.start - 1]
                    prev_token2 = doc[ent.start - 2]
                    if  prev_token1.dep == prep and prev_token2.lemma_ in ("arrive", "there"):
                        ticketdict.update({"departure_condition": "arr"})
                        ticketdict.update({"departure_time": timeFormat(ent.text)})
                    else:
                        ticketdict.update({"departure_condition": "dep"})
                        ticketdict.update({"departure_time": timeFormat(ent.text)})

        #find num_adults and children
        if ent.label_ == "CARDINAL" and ent.start != len(doc) - 1:
            next_token = doc[ent.start + 1]
            if  next_token.lemma_ in ("adult"):
                ticketdict.update({"num_adults": ent.text})
            if  next_token.lemma_ in ("child", "kid"):
                ticketdict.update({"num_children": ent.text})

        #returning
        if (returning == True and ent.start > tokenReturning) or returningInput == True:

            #find return date
            if ent.label_ == "DATE":
                ticketdict.update({"return_date": dateFormat(ent.text)})

            #find return condition or time
            if ent.label_ == "TIME":
                if ent.start != 0: 
                    prev_token1 = doc[ent.start - 1]
                    prev_token2 = doc[ent.start - 2]
                    if  prev_token1.dep_ == "prep" and (prev_token2.lemma_ in ("arrive", "there")):
                        ticketdict.update({"return_condition": "arr"})
                        ticketdict.update({"return_time": timeFormat(ent.text)})
                    else:
                        ticketdict.update({"return_condition": "dep"})  
                        ticketdict.update({"return_time": timeFormat(ent.text)})

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #experimental final pass to find possible named entities missed by large prediction model
    # final pass to find potentially missed times in format hh:mm if there are missing departure date or time information
    if (ticketdict.get("departure_time") == None) or (ticketdict.get("departure_date") == None):
        for token in doc:
            #try to find missed out departure times
            if (returning == True and token.i < tokenReturning) or (returningInput == True) or (returning != True and returningInput != True) :
                if (re.search('\d{,2}:\d{,2}', token.text) is not None):
                    if ent.start != 0:
                        prev_token1 = doc[ent.start - 1]
                        prev_token2 = doc[ent.start - 2]
                        if  prev_token1.dep == prep and prev_token2.lemma_ in ("arrive", "there"):
                            ticketdict.update({"departure_condition": "arr"})
                            ticketdict.update({"departure_time": timeFormat(token.text)})
                        else:
                            ticketdict.update({"departure_condition": "dep"})
                            ticketdict.update({"departure_time": timeFormat(token.text)})
            #or try to find out missing date time       
            if (re.search('\d{,2}/\d{,2}(?/\d{,2})', token.text) is not None):
                #add formatting for dd/mm/yy here
                ticketdict.update({"return_date": dateFormat2(token.text)})
    
    #if there are missing values for return ticket when return is specified try to look
    if (ticketdict.get("returning") == True) and ((ticketdict.get("return_date") == None) or (ticketdict.get("return_time") == None)):
        for token in doc:
            #find the return time and aswell if missing
            if (returning == True and token.i > tokenReturning) or returningInput == True:
                    if (re.search('\d{,2}:\d{,2}', token.text) is not None):
                        if ent.start != 0:
                            prev_token1 = doc[ent.start - 1]
                            prev_token2 = doc[ent.start - 2]
                            if  prev_token1.dep == prep and prev_token2.lemma_ in ("arrive", "there"):
                                ticketdict.update({"return_condition": "arr"})
                                ticketdict.update({"return_time": timeFormat(token.text)})
                            else:
                                ticketdict.update({"return_condition": "dep"})  
                                ticketdict.update({"return_time": timeFormat(token.text)})

            if (re.search('\d{,2}/\d{,2}(/\d{,2})?', token.text) is not None):
                ticketdict.update({"return_date": dateFormat2(token.text)})

    return ticketdict

def predictionNLP(input):

    doc = nlp(input)
    predictiondict = {
        "departing_from": None,
        "departing_to": None,
        "departure_date": None,
        "departure_time": None,
        "previous_delay": None 
    }

    for ent in doc.ents:

        if ent.label_ == "TIME":
            if ent.start != 0:
                prev_token1 = doc[ent.start - 1]
                prev_token2 = doc[ent.start - 2]
                if  (prev_token1.lemma_ in ("delay")) or (prev_token2.lemma_ in ("delay")):
                    time = ent.text
                    time = re.sub("[^0-9]", '', time)
                    delaytime = int(time)
                    predictiondict.update({"previous_delay": delaytime})

        if ent.label_ == "GPE":
                if ent.start != 0:
                    prev_token = doc[ent.start - 1]
                    if prev_token.lemma_ in ("from", "depart"):
                        predictiondict.update({"departing_from": ent.text})
                    if prev_token.lemma_ in ("to", "at"):
                        predictiondict.update({"departing_to": ent.text})

    return predictiondict

def timeFormat(input):
    strtime = input
    if (re.search(r'\d{,2}\:\d{,2}\s?(?:AM|PM|am|pm)', input) is not None):
        strtime = strtime[:-2]
        in_time = datetime.strptime(strtime, "%I:%M")
        out_time = datetime.strftime(in_time, "%H%M")
        return out_time
    else:
        in_time = datetime.strptime(strtime, "%H:%M")
        out_time = datetime.strftime(in_time, "%H%M")
        return out_time 

'''def dateFormat(input):
    date = input
    date = re.sub("[^0-9]", '', date)
    datenew = datetime.now()
    depdate = datenew.replace(day = int(date), hour = 0, minute = 0, second = 0).strftime('%d%m%y')
    return depdate'''

'''def timeFormat2(input):
    strtime = input
    in_time = datetime.strptime(strtime, "%I:%M")
    out_time = datetime.strftime(in_time, "%H%M")
    return out_time'''

def dateFormat2(input):
    date = input
    datenew = None
    #check for if date is DD/MM or DD/MM/YY
    #for DD/MM/YY
    if (re.search(r'\d{,2}\/\d{,2}\/\d{,2}', date) is not None):
        datenew = datetime.strptime(date, '%d/%m/%y')
    #For DD/MM which assumes this year
    if (re.search(r'\d{,2}\/\d{,2}', date) is not None):
        strarr = date.split("/")
        datetemp = datetime.now()
        datenew = datetemp.replace(day = int(strarr[0]), month = int(strarr[1]), hour = 0, minute = 0, second = 0).strftime('%d%m%y')
    return datenew



print(inputNLP("I want a ticket on the 15/01/20 from Norwich to Cambridge arriving at 5:00pm and i want a return ticket for the 18/01 leaving at 14:00"))
