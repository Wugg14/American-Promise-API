import datetime
import constants
from datetime import timedelta
from simple_salesforce import Salesforce

sf = Salesforce(username= constants.SF_USER_NAME, password= constants.SF_PASSWORD, security_token= constants.SF_SECURITY_TOKEN)

#finds the salesforce account ID
def find_account_id(email):
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
def create_new_opportunity(ID, amount, reoccurenceType):
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
        'Designation__c': 'C4'
	})
    return 'Success!'
    



    


