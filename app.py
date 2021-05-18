import schedule
import requests
import time
import smtplib


server = smtplib.SMTP_SSL("smtp.gmail.com", 462)
server.login("Sender_email_address", "Email_password")

user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
'Safari/537.36'


def get_center_data():
    headers = {
    'User-Agent': user_agent_desktop,
    'Accept-Language': 'en_US',
    'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
        'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=130&date=18-05-2021',
        headers = headers
    )
    except Exception:
        print("Error")

    res = response.json()

    ok = False
    
    var_list = {}

    for i in res['centers']:
        for j in i['sessions']:
            if int(j['available_capacity']) > 0 and int(j['min_age_limit']) == 18:
                var_list[i['name']] = j['slots']
                ok = True
    if ok == True:
        print('Vaccine is available')
    return var_list



 server.sendmail("Sender_email_address",
                 "Receiver_email_address",
                 "Vaccine is available. Please book")


schedule.every(1).minutes.do(get_center_data)

while True:
    print("sleeping")
    schedule.run_pending()
    time.sleep(20)


server.quit()

