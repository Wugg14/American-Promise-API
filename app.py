from flask import Flask, request #import main Flask class and request object
from transactionDetails import get_transaction_details, get_reoccurence_type #import transaction details, GET request to Authorize.net and reoccurence type function
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
    amount = req_data['payload']['authAmount']
    authorizeID = req_data['payload']['id']
    authorizeData = get_transaction_details(authorizeID)
    email = authorizeData['transaction']['customer']['email']
    if check_subscription_key(authorizeData['transaction']) == True:
        #get the authorize subscription ID to determine the reoccurence type
        subscriptionID = authorizeData['transaction']['subscription']['id']
        PayNum = authorizeData['transaction']['subscription']['payNum']
        reoccurenceType = get_reoccurence_type(subscriptionID)
        #find salesforce ID
        SFID = find_account_id(email) #Salesforce ID
        #make new opportunity record
        create_new_opportunity(SFID, amount, reoccurenceType, PayNum)
        app.logger.info('Created Opportunity for SFID' + SFID)
        return "Success!"
    else:
        app.logger.info('Not a Sub')
        return "Error: Not a Subscription"
    
    

def check_subscription_key(dict):
    if 'subscription' in dict: 
        return True
    else: 
        return False
	
if __name__ == '__main__':
	app.run(debug=True, port=5000)


