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
    if req.get("result").get("action") != "costo.risorsa":
        return {
            "speech": "no action",
            "displayText": "no action",
            "source": "apiai-onlinestore-shipping"
        }
    result = req.get("result")
    parameters = result.get("parameters")
    #zone = parameters.get("shipping-zone")
    esperienza = parameters.get("esperienza_fra")
    provenienza = parameters.get("provenienza_fra")
    risorsa = provenienza + " " + esperienza

    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    cost = {'interna junior':150, 'interna senior':250, 'esterna junior':180, 'esterna senior':210}

    contexts = result.get("contexts")
    user = ""
    length = range(len(contexts))
    for i in length:
        context = contexts[i]
        lista_par  = context['parameters']
        for p in lista_par:
            if p == "utente.original"
                user = lista_par[p]


    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech = "Ciao " + user + ", il costo di una risorsa " + risorsa + " is " + str(cost[risorsa]) + " euro."

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
