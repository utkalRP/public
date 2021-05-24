from datetime import datetime, timedelta
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Enter one or more PIN codes separated by comma, ex: ['123456', '654321']
pins = ['500019','502032']

#Enter for how many days you want to search from today
advDay = 30

st = datetime.now()
header = {'Accept-Language': 'hi_IN', 'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

try:
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
                print('Avilable slot on {}'.format(day))
                print('-' * 80)
                for k in ['name','address', 'state_name', 'district_name', 'block_name', 'pincode', 'fee_type', 'available_capacity_dose1', 'available_capacity_dose2', 'fee', 'min_age_limit', 'vaccine', 'slots']:
                    print('%-25s : %s' % (k.title(), s[k]))
                print()
except Exception as e:
    print(str(e))
    
