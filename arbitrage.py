import os
import time
from luno_python.client import Client
import requests
from requests.auth import HTTPBasicAuth

if __name__ == '__main__':
    saAccount = Client(api_key_id='bdc6udywrcxdy',
               api_key_secret='6QhflvPxdqrhRDo1VU-qw3sdZXwCLlTCOIGBWyOkfeY')
    itAccount = Client(api_key_id='bdc6udywrcxdy',
               api_key_secret='6QhflvPxdqrhRDo1VU-qw3sdZXwCLlTCOIGBWyOkfeY')

    ##### Pre test for accounts are ready #########
    res = saAccount.get_balances()
    saBTC = ''
    saZAR = ''
    if res['balance']:
        for bal in res['balance']:
            if bal['asset'] == 'XBT':
                saBTC = bal['account_id']
            elif bal['asset'] == 'ZAR':
                saZAR = bal['account_id']

    res = itAccount.get_balances()
    itBTC = ''
    itEuro = ''
    if res['balance']:
        for bal in res['balance']:
            if bal['asset'] == 'XBT':
                itBTC = bal['account_id']
            elif bal['asset'] == 'EUR':
                itEuro = bal['account_id']
    print(saBTC, saZAR, itBTC, itEuro)
    #######################

    #### main logic #####
    while True:
        ## get exchange rate between zar and euro
        response = requests.get("https://xecdapi.xe.com/v1/convert_from/?from=EUR&to=ZAR&amount=1", auth=HTTPBasicAuth('liming419944535', 'qajfi3hr0ug3g71ulc3n25ben8'))
        if response.status_code == 200:
            xrateJson = response.json()
            xrate = xrateJson['to'][0]['mid']
            print(xrate)
        ##res = saAccount.list_user_trades(pair='XBTZAR')
        ##print(res)
        time.sleep(1)
    
    