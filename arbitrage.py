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
        xrate = 0
        if response.status_code == 200:
            xrateJson = response.json()
            xrate = float(xrateJson['to'][0]['mid'])
            print(xrate)
        else:
            print("Can't fetch exchange rate, wait until get exact exchange rate ....")
            continue
        
        res = saAccount.get_ticker(pair='XBTZAR')
        _br = float(res['last_trade']) # BTC to ZAR
        res = itAccount.get_ticker(pair='XBTEUR')
        _be = float(res['last_trade']) # BTC to EURO
        print(_br, _be)
        arbitrageRate = (_br - _be * xrate) / (_be * xrate) * 100.0
        print( "arbitrageRate", arbitrageRate)
        
        ## when arbitrage rate is below than 1%, then send BTC to italy
        if arbitrageRate < 2:            
            res = saAccount.get_balances(assets='ZAR')
            saZarBalance = res["balance"][0]["balance"]
            saZAR = res["balance"][0]["account_id"]            
            try:
                orderResp = saAccount.post_market_order(pair="XBTZAR", type="BUY", counter_account_id=saZAR, counter_volume=saZarBalance)
                orderId = orderResp["order_id"]
                while True:
                    orderDetail = saAccount.get_order(orderId)
                    print("Waiting for Buy BTC in South After....", orderId, orderDetail['state'])
                    if orderDetail['state'] == 'COMPLETE':
                        break
                    time.sleep(10)
            except Exception as e:
                print("Error while buying BTC in South Africa", e)
        ##res = saAccount.list_user_trades(pair='XBTZAR')
        ##print(res)
        time.sleep(1)
    
    