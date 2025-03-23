import pandas as pd
import numpy as np



def backtest(df:pd.DataFrame,ma_perioid:int):

    df["obv"] = np.sign(df["close"].diff())
    print(df)



