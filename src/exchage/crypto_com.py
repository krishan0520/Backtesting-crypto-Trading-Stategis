from typing import *
import requests
import logging

logger = logging.getLogger()

class CryptocomClient:
    def __init__(self):
        


        self._base_url = 'https://api.crypto.com/v2'
  

        self.symbols = self._get_symbols()


    def _make_request(self,endpoint:str,query_parameters:Dict):

        try:
            response = requests.get(self._base_url+endpoint,params=query_parameters)

        except Exception as e:
            logger.error("Connection error while making request to %s: %s",endpoint,e)
            return None

        if response.status_code ==200:
            return response.json()
        
        else:
            logger.error("Error while making request to %s: %s (status code=%s)",endpoint,response.json(),response.status_code)
            return None
        

    def _get_symbols(self):
        params = dict()
        endpoint = "/public/get-instruments"

        data= self._make_request(endpoint,params)

        if data and  data.get("result"):


            instruments = data["result"].get("instruments",[])
            symbols = [x["instrument_name"] for x in instruments]
            return symbols
        else:
            symbols = []

    def get_historical_data(self,symbol:str,start_time:Optional[int]=None,end_time:Optional[int]=None,count:Optional[int]=None):
        params = dict()
        params["instrument_name"] = symbol
        params["timeframe"] = 'M1'



        if symbol not in self.symbols:
            logger.error("Symbol %s is not available",symbol)
            return None 
        
        if start_time is not None:
            params["start_ts"] = start_time
        if end_time is not None:
            params["end_ts"] = end_time
        if count is not None:
            params["count"] = count

        endpoint = "/public/get-candlestick"
        data =self._make_request(endpoint,params)

        if not data:
            return None
        
        if data.get("result"):

            candles = []
              

            for c in data["result"]["data"]:

                candles.append((float(c["t"]),float(c["o"]),float(c["h"]),float(c["l"]),float(c["c"]),float(c["v"])))
            return candles
        else:
            logger.error("Error with fetching candlestick data for %s",symbol)
            return None





    


        
    

