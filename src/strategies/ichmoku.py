import pandas as pd
import numpy as np



pd.set_option("display.max_columns",None)
#pd.set_option("display.max_rows",None)
pd.set_option("display.width",1000)


def backtest(df :pd.DataFrame,tenkan_period:int,kijun_period:int):

    #Tenkan sen : short-term signal line

    df["rolling_min_tenkan"] = df["low"].rolling(window=tenkan_period).min()
    df["rolling_max_tenkan"] = df["high"].rolling(window=tenkan_period).max()

    df["tenkan_sen"] =  (df["rolling_min_tenkan"] +df["rolling_max_tenkan"])/2

    df.drop(["rolling_min_tenkan","rolling_max_tenkan"],axis=1,inplace=True)

    #Kijun sen : short-term signal line

    df["rolling_min_kijun"] = df["low"].rolling(window=kijun_period).min()
    df["rolling_max_kijun"] = df["high"].rolling(window=kijun_period).max()

    df["kijun_sen"] =  (df["rolling_min_kijun"] +df["rolling_max_kijun"])/2

    df.drop(["rolling_min_kijun","rolling_max_kijun"],axis=1,inplace=True)


    #senkou span A


    df["senkou_span_a"] = ((df["tenkan_sen"]+df["kijun_sen"])/2).shift(kijun_period)

    #senku span B
    

    df["rolling_min_senkou"] = df["low"].rolling(window=kijun_period*2).min()

    df["rolling_max_senkou"] = df["high"].rolling(window=kijun_period*2).max()

    df["senkou_span_b"] = ((df["rolling_min_senkou"]+df["rolling_max_senkou"])/2).shift(kijun_period)

    df.drop(["rolling_min_senkou","rolling_max_senkou"],axis=1,inplace=True)


    #chiku span:confirmation line

    df["chinku_span"] = df["close"].shift(kijun_period)

    df.dropna(inplace=True)




    #signal

    df["tenkan_minus_kijun"] = df["tenkan_sen"] - df["kijun_sen"]
    df["prev_tenkan_minus_kijun"] = df["tenkan_minus_kijun"].shift(1)

    df["signal"] = np.where((df["tenkan_minus_kijun"]>0) & 
                             (df["prev_tenkan_minus_kijun"] <0 ) &
                            (df["close"]>df["senkou_span_a"]) &
                            (df["close"]>df["senkou_span_b"]) &
                            (df["close"]>df["chinku_span"]),1,
                            
                            np.where((df["tenkan_minus_kijun"]<0) & 
                             (df["prev_tenkan_minus_kijun"] >0 ) &
                            (df["close"]<df["senkou_span_a"]) &
                            (df["close"]<df["senkou_span_b"]) &
                            (df["close"]<df["chinku_span"]),-1,0))

    
    #only incl7uding 1 or -1 as signal data removing 0 which has no decion

    signal_data = df[df["signal"] !=0].copy()

    signal_data["pnl"] = signal_data["close"].pct_change()*signal_data["signal"].shift(1)

    return signal_data["pnl"].sum()


