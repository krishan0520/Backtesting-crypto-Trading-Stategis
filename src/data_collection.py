from exchage.binance import BinannceClient
from exchage.crypto_com import CryptocomClient

from typing import *

from utils import *

import time 

import logging

logger = logging.getLogger()

def all_data(client:Union[BinannceClient,CryptocomClient],exchange:str,symbol:str):

    oldest_ts,most_ts = None,None

    #inital request

    if oldest_ts is None:

        data = client.get_historical_data(symbol , end_time= int(time.time()*1000-60000))

        if len(data)== 0:
            logger.warning("%s %s : no intital data found ", exchange,symbol)
            return 
        
        else:
            logger.info("%s %s: Collected %s intial data from %s to %s ", exchange,symbol,len(data),ms_to_dt(data[0][0]),ms_to_dt(data[-1][0]))







    
    pass