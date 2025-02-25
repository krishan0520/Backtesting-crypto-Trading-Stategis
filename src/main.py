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
    
    


    


    