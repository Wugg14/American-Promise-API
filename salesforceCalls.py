import datetime
import constants
from datetime import timedelta
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
def create_new_opportunity(ID, amount, reoccurenceType, PayNum):
    sf = Salesforce(username= constants.SF_USER_NAME, password= constants.SF_PASSWORD, security_token= constants.SF_SECURITY_TOKEN)
    #format dating
    fmt = '%Y-%m-%dT%H:%M:%S'
    d = datetime.datetime.now()
    #Create opportunity
    sf.Opportunity.create(
        {
        'AccountId':ID,
	'Amount':amount,
        'Name':'Default Flask App Value',
	'StageName':'Closed Won',
	'Type': 'Donation',
	'CloseDate':d.strftime(fmt),
	'OwnerId':'005f2000006uFa3AAE',
        'Payment_Method__c': 'Credit Card',
        'Reoccurence_Type__c': reoccurenceType,
        'Designation__c': 'C4',
        'Recurring_Donation_Number__c': PayNum
	})
    return 'Success!'
    



    


