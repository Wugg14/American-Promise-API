from flask import Flask, request #import main Flask class and request object
from transactionDetails import get_transaction_details, get_reoccurence_type, get_subscription_details #import transaction details, GET request to Authorize.net and reoccurence type function
from salesforceCalls import find_account_id, create_new_opportunity  #import salesforce API requests

app = Flask(__name__) #create the Flask app

#Hello World test for root of app
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/json', methods=['POST']) #GET requests will be blocked
def incoming_json():
    req_data = request.get_json(force=True)
    app.logger.info('received JSON')
    app.logger.info(req_data)
    try:
        amount = req_data['payload']['authAmount']
        authorizeID = req_data['payload']['id']
        authorizeDate = req_data['eventDate']
        authorizeData = get_transaction_details(authorizeID)
        if 'transaction' in authorizeData:
            customer = authorizeData['transaction']['customer']
            if 'email' in customer:
                email = authorizeData['transaction']['customer']['email']
            else:
                return "Authorize did not provide necessary email"
        else:
            return "Authorize did not provide necessary customer information"

    except KeyError:
        return "Payload did not include necessary data"

    if (check_subscription_key(authorizeData['transaction']) == True):
        #get the authorize subscription ID to determine the reoccurence type
        subscriptionID = authorizeData['transaction']['subscription']['id']
        PayNum = authorizeData['transaction']['subscription']['payNum']
        if PayNum != 1:
            reoccurenceType = get_reoccurence_type(subscriptionID)
            subInfo = get_subscription_details(subscriptionID)
            email = subInfo['subscription']['profile']['email']
            #find salesforce ID
            try:
                print(email)
                SFID = find_account_id(email) #Salesforce ID
            except:
                app.logger.info("Salesforce Error, Authorize Transaction ID: " + authorizeID)
                return "Salesforce Error"
            #make new opportunity record
            create_new_opportunity(SFID, amount, reoccurenceType, PayNum, authorizeID, subscriptionID, authorizeDate)
            app.logger.info('Created Opportunity for SFID' + SFID)
            return "Success!"
        else:
            app.logger.info('Handled by Zapier')
            return "Did not create record, handled by Zapier"
    else:
        if authorizeData['transaction']['recurringBilling'] == True:
            app.logger.info('AUTHORIZE API SUB GLITCH PLEASE FIX')
            app.logger.info(authorizeData['transaction'])
            return "Authorize API Issue"

        else:
            app.logger.info('Not a Sub')
            app.logger.info(authorizeData['transaction'])
            return "Error: Not a Subscription"

def check_subscription_key(dict):
    if 'subscription' in dict: 
        return True
    else: 
        return False
	
if __name__ == '__main__':
	app.run(debug=True, port=5000)


