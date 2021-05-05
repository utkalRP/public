from datetime import datetime, timedelta
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Enter one or more PIN codes separated by comma, ex: ['123456', '654321']
pins = ['500019']

#Enter for how many days you want to search from today
advDay = 10

st = datetime.now()
header = {'Accept-Language': 'hi_IN', 'accept': 'application/json'}

for pin in pins:
    for i in range(0, advDay+1):
        day = (st + timedelta(days = i)).strftime('%d-%m-%Y')
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=' + pin + '&date=' + day
        res = requests.get(url, params={}, headers=header, verify=False)
        resList = json.loads(res.text)
        if len(resList['sessions']) == 0:
            print(f'No slots available for PIN: {pin} and Date: {day}')
        for s in resList['sessions']:
            print(f'Avilable slot on {day}:\nAddress:\t{s["name"]}, {s["address"]}, {s["block_name"]}, {s["district_name"]}, {s["state_name"]}\nSlots:\t\t{s["slots"]}\nFee Type:\t{s["fee_type"]}\nFee:\t\t{s["fee"]}\nCapacity:\t{s["available_capacity"]}\nMin Age:\t{s["min_age_limit"]}\nVaccine:\t{s["vaccine"]}\n')
