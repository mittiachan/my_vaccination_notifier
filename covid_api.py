import requests
import json
from twilio.rest import Client
import schedule
import time

state_ids = {"states":[{"state_id":1,"state_name":"Andaman and Nicobar Islands"},{"state_id":2,"state_name":"Andhra Pradesh"},{"state_id":3,"state_name":"Arunachal Pradesh"},{"state_id":4,"state_name":"Assam"},{"state_id":5,"state_name":"Bihar"},{"state_id":6,"state_name":"Chandigarh"},{"state_id":7,"state_name":"Chhattisgarh"},{"state_id":8,"state_name":"Dadra and Nagar Haveli"},{"state_id":37,"state_name":"Daman and Diu"},{"state_id":9,"state_name":"Delhi"},{"state_id":10,"state_name":"Goa"},{"state_id":11,"state_name":"Gujarat"},{"state_id":12,"state_name":"Haryana"},{"state_id":13,"state_name":"Himachal Pradesh"},{"state_id":14,"state_name":"Jammu and Kashmir"},{"state_id":15,"state_name":"Jharkhand"},{"state_id":16,"state_name":"Karnataka"},{"state_id":17,"state_name":"Kerala"},{"state_id":18,"state_name":"Ladakh"},{"state_id":19,"state_name":"Lakshadweep"},{"state_id":20,"state_name":"Madhya Pradesh"},{"state_id":21,"state_name":"Maharashtra"},{"state_id":22,"state_name":"Manipur"},{"state_id":23,"state_name":"Meghalaya"},{"state_id":24,"state_name":"Mizoram"},{"state_id":25,"state_name":"Nagaland"},{"state_id":26,"state_name":"Odisha"},{"state_id":27,"state_name":"Puducherry"},{"state_id":28,"state_name":"Punjab"},{"state_id":29,"state_name":"Rajasthan"},{"state_id":30,"state_name":"Sikkim"},{"state_id":31,"state_name":"Tamil Nadu"},{"state_id":32,"state_name":"Telangana"},{"state_id":33,"state_name":"Tripura"},{"state_id":34,"state_name":"Uttar Pradesh"},{"state_id":35,"state_name":"Uttarakhand"},{"state_id":36,"state_name":"West Bengal"}],"ttl":24}
district_id = {'Bangalore Urban': 265, 'BBMP': 294}     # 'Thrissur': 303, 'Bangalore Rural': 276,

account_sid = "AC4a940418968a502af61d2d2ddd5b9d2b"
auth_token = "7eb7bf767d2d3a32a605871a08bd2f4d"

members = [
        {"phone_number": "+919629438603", "name": "Mike"},
    ]

records = {}
available_sessions = []


def check_data(data):
    if len(data['centers']) > 0:
        for center in data['centers']:
            # print(center['name'], ', ', center['address'], ', ', len(center['sessions']))
            if len(center['sessions']) > 0:
                for session in center['sessions']:
                    if session['min_age_limit'] == 18 and session['available_capacity_dose1'] >= 3:
                        available_sessions.append(f"""district: {center['district_name']}, place: {center['name']}, {center['address']}
date: {session['date']}, total_doses: {session['available_capacity']}, age: {session['min_age_limit']}+, dose_1: {session['available_capacity_dose1']}
""")
                        print(f"""district: {center['district_name']}, place: {center['name']}, {center['address']}
    date: {session['date']}, total_doses: {session['available_capacity']}, age: {session['min_age_limit']}+, dose_1: {session['available_capacity_dose1']}""")
            else:
                pass
                # print('no sessions available')


def run_test():
    print('Checking!!!')
    browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    api_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
    for key in district_id.keys():
        print('loading data for ', key)
        api_params = {'date': '30-05-2021', 'district_id': district_id[key]}
        response = requests.get(api_url, headers=browser_header, params=api_params)
        records[key] = json.loads(response.text)

    for d in records.values():
        if d:
            check_data(d)

    client = Client(account_sid, auth_token)

    if len(available_sessions) > 0:
        for member in members:
            client.messages.create(to=member['phone_number'], from_="+18782160564",
                                    body=f"""
There is a vaccine availability in the below places:
{' '.join(available_sessions)}""")
            client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml',
                to=member['phone_number'],
                from_='+18782160564')
        available_sessions.clear()
    else:
        print('done checking........no vaccines available currently', end='\n')



schedule.every(5).minutes.do(run_test)

# schedule.every().hour.do(run_test())

while 1:
    schedule.run_pending()
    time.sleep(1)

# else:
#     for member in members:
#         message = client.messages.create(to=member['phone_number'], from_="+18782160564",
#                                          body=f"""There are no sessions available as of now in Thrissur on {api_params['date']}.""")
