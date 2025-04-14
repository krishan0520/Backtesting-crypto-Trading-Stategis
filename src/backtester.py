from data_collection import Hdf5Client
import strategies.ichmoku
import strategies.support_res
from utils import*

import strategies.obv



def run(exchange:str,strategy:str,symbol:str,tf:str,from_time:int,to_time:int):


    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol,from_time,to_time)
        data = resample_timeframe(data,tf)

        print(strategies.obv.backtest(data,9))

    elif strategy=="ichmoku":

        h5_db = Hdf5Client(exchange)
        data =h5_db.get_data(symbol,from_time,to_time)
        data = resample_timeframe(data,tf)

        print(strategies.ichmoku.backtest(data,tenkan_period=9,kijun_period=26))


    elif strategy=="sup_res":

        h5_db = Hdf5Client(exchange)
        data =h5_db.get_data(symbol,from_time,to_time)
        data = resample_timeframe(data,tf)

        print(strategies.support_res.backtest(data,min_point=3,min_diff_point=7,rounding_num=200,profit_take=3,stop_loss=3))









    

