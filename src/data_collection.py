from exchage.binance import BinannceClient
from exchage.crypto_com import CryptocomClient
from database import Hdf5Client

from typing import *

from utils import *

import time 

import logging

logger = logging.getLogger()

def all_data(client:Union[BinannceClient,CryptocomClient],exchange:str,symbol:str):

    hf5_db = Hdf5Client(exchange)
    hf5_db.create_datasets(symbol)

    oldest_ts,most_ts = hf5_db.get_first_last_timestamp(symbol)
    print(oldest_ts,most_ts)


    #inital request

    if oldest_ts is None:

        data = client.get_historical_data(symbol , end_time= int(time.time()*1000-60000))

        if len(data)== 0:
            logger.warning("%s %s : no intital data found ", exchange,symbol)
            return 
        
        else:
            logger.info("%s %s: Collected %s intial data from %s to %s ", exchange,symbol,len(data),ms_to_dt(data[0][0]),ms_to_dt(data[-1][0]))


        
        oldest_ts = data[0][0]
        most_ts = data[-1][0]

        hf5_db.write_data(symbol,data)



        #Most recent data

    while True:


       data = client.get_historical_data(symbol,start_time= int(most_ts + 60000))

       if data is None:
            time.sleep(4) #pause in case error occurs during the request
            continue
       if len(data)<2:
           break

       
       data = data[:-1]
       
       if data[-1][0]>most_ts:
        most_ts = data[-1][0]
        

        logger.info("%s %s: Collected  %s recent data from %s to %s ", exchange,symbol,len(data),ms_to_dt(data[0][0]),ms_to_dt(data[-1][0]))
        
        hf5_db.write_data(symbol,data)

        time.sleep(1.1)


    #older data

    while True:


        data = client.get_historical_data(symbol,end_time=int(oldest_ts - 60000))

        if data is None:
           time.sleep(4) #pause in case error occurs during the request
           continue
        if len(data) == 0:
           
           logger.info("%s %s Stopped older data collection beacause no data was found before %s",exchange,symbol,ms_to_dt(oldest_ts))
           break

           
       

       
        if data[0][0]<oldest_ts:
           oldest_ts = data[0][0]

           logger.info("%s %s: Collected  %s older data from %s to %s ", exchange,symbol,len(data),ms_to_dt(data[0][0]),ms_to_dt(data[-1][0]))

           hf5_db.write_data(symbol,data)

           time.sleep(1.1)


          


    
       












    
    