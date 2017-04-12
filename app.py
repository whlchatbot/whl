#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    action = req.get("result").get("action")
    res =  {
            "speech": "no action",
            "displayText": "no action",
            "source": "apiai-onlinestore-shipping"
        }
    print("Action:")
    print(action)
    if (action == "costo.risorsa"):
        res =  costorisorsa(req)
        
    if (action == "quantita.risorsa"):
        res = quantitarisorsa(req)
    
    return res
    
    
def quantitarisorsa(req):
    result = req.get("result")
    parameters = result.get("parameters")
    #zone = parameters.get("shipping-zone")
    esperienza = parameters.get("esperienza_fra")
    provenienza = parameters.get("provenienza_fra")
    risorsa = provenienza + " " + esperienza
    print("Response:")
    print(esperienza+" "+risorsa)
    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    quantita = {'interna junior':55, 'interna senior':22, 'esterna junior':33, 'esterna senior':11}

    contexts = result["contexts"]
    user = ""
    for context in contexts:
        parameters = context['parameters']
        for p in parameters:
            if p == "utente.original":
                user = parameters.get("utente.original")

    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech = user + " le risorse " + risorsa + " sono "+str(quantita[risorsa])
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
def costorisorsa(req):
    result = req.get("result")
    parameters = result.get("parameters")
    #zone = parameters.get("shipping-zone")
    esperienza = parameters.get("esperienza_fra")
    provenienza = parameters.get("provenienza_fra")
    risorsa = provenienza + " " + esperienza

    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    cost = {'interna junior':150, 'interna senior':250, 'esterna junior':180, 'esterna senior':210}

    contexts = result["contexts"]
    user = ""
    for context in contexts:
        parameters = context['parameters']
        for p in parameters:
            if p == "utente.original":
                user = parameters.get("utente.original")

    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech = user + " una risorsa " + risorsa + " costa " + str(cost[risorsa]) + " euro."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
