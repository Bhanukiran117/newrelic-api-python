import requests
import json

 
AUTH_TOK = 'NRA-xxxxxxxxxxxxxxx'  # For Put requests you have get admin API Token, else you get permission denied.
HEADERS = {
    'X-Api-Key': '{0}'.format(AUTH_TOK),
    'Content-type': 'application/json',
}

incident_data_dict = {}
list_alerts_violations ={}



def get_incident(incident_number):
    ivars = dict()
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_incidents"
    ivars['incident_number'] = incident_number
    results = requests.get(
    '{base_url}/{incident_number}.json'.format(**ivars),
    headers=HEADERS
    )
    return results.json() if results.status_code == 200 else "{'data':'Not found'}"
   
def list_alerts_violations(start_date,end_date,only_open):
    ivars = dict()
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_violations.json"
    var_params = {
        "start_date" : start_date,
        "end_date" : end_date,
        "only_open" : only_open
    }
    results = requests.get(
    '{base_url}'.format(**ivars),
    headers=HEADERS,
    params=var_params
    )
    return results.json() if results.status_code == 200 else "{'data':'Not found'}"
    

incident_data_dict = get_incident(130772850)
#print(incident_data_dict)

list_alerts_violations = list_alerts_violations(start_date="2020-05-25T16:55:00+00:00",end_date="2020-05-27T16:56:00+00:00",only_open="true")
#print(list_alerts_violations)
for violations in list_alerts_violations['violations']:
    print(violations['links']['incident_id'])
    


def post_incident_ack(incident_number):
    ivars = dict()
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_incidents"
    ivars['incident_number'] = incident_number
    results = requests.put(
    '{base_url}/{incident_number}/acknowledge.json'.format(**ivars),
    headers=HEADERS
    )
    return "Successful Ack" if results.status_code == 200 else "Failure Ack"


def post_incident_close(incident_number):
    ivars = dict()
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_incidents"
    ivars['incident_number'] = incident_number
    results = requests.put(
    '{base_url}/{incident_number}/close.json'.format(**ivars),
    headers=HEADERS
    )
    return "Close Successful" if results.status_code == 200 else "Close Successful"

for violations in list_alerts_violations['violations']:
    #print(violations['links']['incident_id'])
    print(violations['links']['incident_id'], post_incident_ack(violations['links']['incident_id']))


for violations in list_alerts_violations['violations']:
    #print(violations['links']['incident_id'])
    print(violations['links']['incident_id'], post_incident_close(violations['links']['incident_id']))
