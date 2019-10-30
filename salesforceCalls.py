import constants
from simple_salesforce import Salesforce

#finds the salesforce account ID
def find_account_id(email):
    sf = Salesforce(username= constants.SF_USER_NAME, password= constants.SF_PASSWORD, security_token= constants.SF_SECURITY_TOKEN)
    #Find Contact
    query = "SELECT Id, Email FROM Contact WHERE Email = "
    queryEmail = "'" + email + "'"
    query = query + queryEmail
    contact = sf.query(query)
    contactID = contact['records'][0]['Id']
    contactDic = sf.Contact.get(contactID)
    accountID = contactDic['AccountId']
    return accountID

#makes a request to salesforce to create the opportunity
def create_new_opportunity(ID, amount, reoccurenceType, PayNum, TransactionID, subscriptionID, date):
    sf = Salesforce(username= constants.SF_USER_NAME, password= constants.SF_PASSWORD, security_token= constants.SF_SECURITY_TOKEN)
    #Create opportunity
    package = sf.Opportunity.create(
        {
        'AccountId':ID,
	    'Amount':amount,
        'Name':'Default Flask App Value',
	    'StageName':'Closed Won',
	    'Type': 'Donation',
	    'CloseDate':date,
	    'OwnerId':'005f2000006uFa3AAE',
        'Payment_Method__c': 'Credit Card',
        'Reoccurence_Type__c': reoccurenceType,
        'Designation__c': 'C4',
        'Recurring_Donation_Number__c': PayNum,
        'Credit_Card_Processor__c': 'Authorize.net',
        'Donation_Unique_External_ID__c': TransactionID,
        'Recurring_Subscription_ID__c': subscriptionID
	})
    return package
     



    


