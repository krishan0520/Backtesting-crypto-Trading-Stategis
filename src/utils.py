import datetime

def ms_to_dt(ms:int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ms/1000,datetime.timezone.utc)