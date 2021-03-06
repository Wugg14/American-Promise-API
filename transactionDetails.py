import requests
import json
import constants

#Makes a request for transaction details to Authorize API
def get_transaction_details(transacationid):
    payload = {
        "getTransactionDetailsRequest": {
            "merchantAuthentication": {
                "name": constants.AUTHORIZE_NAME,
                "transactionKey": constants.AUTHORIZE_TRANSACTION_KEY
            },
            "transId": transacationid
        }
    }
    header = {'Content-Type': 'application/json'}
    r = requests.post("https://api.authorize.net/xml/v1/request.api", json = payload, headers = header)
    r = r.text
    text = r.encode('utf8')[3:].decode('utf8')
    info = json.loads(text)
    return info

#Makes a request for subscription details to Authorize API
def get_subscription_details(subscriptionid):
    payload = {
      "ARBGetSubscriptionRequest": {
        "merchantAuthentication": {
          "name": constants.AUTHORIZE_NAME,
          "transactionKey": constants.AUTHORIZE_TRANSACTION_KEY
        },
        "subscriptionId": subscriptionid,
        "includeTransactions": 'false'
      }
    }
    header = {'Content-Type': 'application/json'}
    r = requests.post("https://api.authorize.net/xml/v1/request.api", json = payload, headers = header)
    r = r.text
    text = r.encode('utf8')[3:].decode('utf8')
    info = json.loads(text)
    return info

#Determines whether a subscription is monthly or yearly
def get_reoccurence_type(subscriptionid):
    data = get_subscription_details(subscriptionid)
    duration = data['subscription']['paymentSchedule']['interval']['length']
    if duration == 1:
        return 'monthly'
    elif duration == 12:
        return 'annual'


def test_get_details():
    payload = {
    "getTransactionDetailsRequest": {
        "merchantAuthentication": {
            "name": constants.AUTHORIZE_NAME,
            "transactionKey": constants.AUTHORIZE_TRANSACTION_KEY
        },
        "transId": 61768997511
    }
    }
    header = {'Content-Type': 'application/json'}
    r = requests.post("https://api.authorize.net/xml/v1/request.api", json=payload, headers=header)
    if str(r) == '<Response [200]>':
        return True
    else:
        return False







