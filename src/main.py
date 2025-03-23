import logging
"""
This script sets up logging for a crypto trading backtesting application and initializes a Binance client.
Modules:
    logging: Provides a way to configure and use loggers.
    exchage.binance: Contains the BinanceClient class for interacting with the Binance exchange.
Logging Configuration:
    - Logs are formatted with timestamps, log level, and message.
    - Logs are output to both the console (INFO level) and a file named 'info.log' (DEBUG level).
Classes:
    BinannceClient: A client for interacting with the Binance exchange.
Functions:
    main: The entry point of the script. Prompts the user to choose a program mode and initializes the Binance client.
Usage:
    Run the script and follow the prompt to choose a program mode (data/backtest/optimize).
"""

from exchage.binance import BinannceClient

from exchage.crypto_com import CryptocomClient

from data_collection import all_data

from utils import*

import datetime

import backtester

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)


logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__=='__main__':

    mode = input("Chose the program mode (data/backtest/optimize): ").lower()

    while True:

       exchange = input("Chose the exchange (binance/crypto_com): ").lower()
       if exchange in ("binance","crypto_com"):
           break
       
    if exchange == "binance":
        client = BinannceClient(True)

    elif exchange == "crypto_com":
        client = CryptocomClient()


    while True:

        symbol = input("Enter symbol:").upper()

        if symbol in client.symbols:
            break 
    
    if mode == "data":
        all_data(client,exchange,symbol)

    elif mode == "backtest":

        avialble_strategies = ["obv"]

        while True:

            strategy = input(f"Chose the strategy: ({', '.join(avialble_strategies)})").lower()
            if strategy in avialble_strategies:
                break

        #Timeframe

        while True:

            tf = input(f"Chose a timeframe: ({', '.join(TF_EQ.keys())})").lower()
            if tf in TF_EQ.keys():
                break
 

        #From time
        
        while True:

            from_time = input("Backtest from (yyyy-mm-dd or press enter:")
            if from_time == "":
                from_time= 0
                break

            try:

                from_time = int(datetime.datetime.strptime(from_time , "%Y-%m-%d").timestamp()*1000)
                break
            except ValueError:
                
                continue
     #To time

        while True:

            to_time = input("Backtest to (yyyy-mm-dd or press enter:")
            if to_time == "":
                to_time= int(datetime.datetime.now().timestamp()*1000)
                break

            try:

                to_time = int(datetime.datetime.strptime(to_time , "%Y-%m-%d").timestamp()*1000)
                break
            except ValueError:
                
                continue
        
        

        backtester.run(exchange,strategy,tf,from_time,to_time)
    
    


    


    