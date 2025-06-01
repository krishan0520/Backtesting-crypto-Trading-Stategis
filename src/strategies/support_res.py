import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
 # or 'Qt5Agg' or 'WebAgg' if you want GUI alternatives


import matplotlib.pyplot as plt
import mplfinance as mpf


pd.set_option("display.max_columns",None)
#pd.set_option("display.max_rows",None)
pd.set_option("display.width",1000)


def backtest(df :pd.DataFrame,min_point:int,min_diff_point :int ,rounding_num:float,profit_take:float,stop_loss:float):

    candle_leg = df.iloc[1].name - df.iloc[0].name

    df["rounded_high"] = round(df["high"] / rounding_num )*rounding_num
    df["rounded_low"]  = round(df["low"] / rounding_num) * rounding_num


    price_group = {"resistances":dict() , "supports":dict()}

    levels = {"resistances":[],"supports":[]}

    support_res = {"resistances": [] , "supports": []}

    for index,row in df.iterrows():

        for side in ["resistances","supports"]:

            h_l = "high" if side == "resistances" else "low"


            if row["rounded_" + h_l] in price_group[side]:

                grp = price_group[side][row["rounded_" + h_l]]

                if grp["start_time"] is None:
                    grp["start_time"] = index


                if grp["last"] is None or index>= grp["last"] + min_diff_point*candle_leg:

                    grp["price"].append(row[h_l])

                    if len(grp["price"])>= min_point:

                        extrem_price = max(grp["price"]) if side == "resistances" else min(grp["price"])

                        levels[side].append([(grp["start_time"],extrem_price),(index,extrem_price)])

                        support_res[side].append({"price":extrem_price, "broken":False})

                    grp["last"] = index

            else:
                price_group[side][row["rounded_" + h_l]] = {"price":[row[ h_l]] , "start_time":index,"last":index}

            
            # check whether price groups are still valide or not

            for key,value in price_group[side].items():

                if len(value["price"])>0:
                    if side == "resistances" and row[h_l] > max(value["price"]):
                        value["price"].clear()
                        value["start_time"] = None
                        value["last"] = None
                    elif side == "supports" and row[h_l] < min(value["price"]):
                        value["price"].clear()
                        value["start_time"] = None
                        value["last"] = None


    

    mpf.plot(df,type="candle",style="charles",warn_too_much_data=len(df)+1000,alines=dict(alines=levels["resistances"]+levels["supports"]))
    plt.savefig("output_plot.png", dpi=300)





            
                





    


    