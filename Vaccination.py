from datetime import datetime, timedelta
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Enter one or more PIN codes separated by comma, ex: ['123456', '654321']
pins = ['500019']

#Enter for how many days you want to search from today
advDay = 30

st = datetime.now()
header = {'Accept-Language': 'hi_IN', 'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

for pin in pins:
    for i in range(0, advDay+1):
        day = (st + timedelta(days = i)).strftime('%d-%m-%Y')
        param = {'pincode':pin, 'date':day}
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin'
        res = requests.get(url, params=param, headers=header, verify=False)
        resList = json.loads(res.text)
        if len(resList['sessions']) == 0:
            print('No slots available for PIN: {} and Date: {}'.format(pin, day))
        for s in resList['sessions']:
            print('Avilable slot on {}:\nAddress:\t{}, {}, {}, {}, {}\nSlots:\t\t{}\nFee Type:\t{}\nFee:\t\t{}\nCapacity:\t{}\nMin Age:\t{}\nVaccine:\t{}\n'.format(day, s["name"], s["address"], s["block_name"], s["district_name"], s["state_name"], s["slots"], s["fee_type"], s["fee"], s["available_capacity"], s["min_age_limit"], s["vaccine"]))
