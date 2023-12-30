import pandas as pd
import time
import requests

import hashlib
import hmac
import base64

from define import const


class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        
        hash.hexdigest()
        return base64.b64encode(hash.digest())
    

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, secret_key)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 
            'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

def getresults(hintKeywords):
    uri = '/keywordstool'
    method = 'GET'

    params={}
    params['hintKeywords']=hintKeywords
    params['showDetail']='1'

    r=requests.get(const.AD_API_BASE_URL + uri, params=params, 
                headers=get_header(method, uri, const.AD_API_API_KEY, const.AD_API_SECRET_KEY, const.AD_API_CUSTOMER_ID))

    return pd.DataFrame(r.json()['keywordList'])