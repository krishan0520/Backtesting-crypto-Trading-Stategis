import datetime
import pandas as pd

TF_EQ = {"1m":"1Min","5m":"5Min","15m":"15Min","30min":"30Min","1h":"1H","4h":"4H","12h":"12H","1d":"D"}

def ms_to_dt(ms:int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ms/1000,datetime.timezone.utc)


def resample_timeframe(data:pd.DataFrame,tf:str)->pd.DataFrame:
    return data.resample(TF_EQ[tf]).agg({"open":"first","high":"max","low":"min","close":"last","volume":"sum"})
