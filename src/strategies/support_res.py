import pandas as pd
import numpy as np



pd.set_option("display.max_columns",None)
#pd.set_option("display.max_rows",None)
pd.set_option("display.width",1000)


def backtest(df :pd.DataFrame,min_point:int,min_diff_point :int ,rounding_num:float,profit_take:float,stop_loss:float):

    candle_leg = df.iloc[1].name - df.iloc[0].name

    df["rounded_high"] = round(df["high"] / rounding_num )*rounding_num
    df["rounded_low"]  = round(df["low"] / rounding_num) * rounding_num


    price_group = {"resistances":dict() , "supports":dict()}

    support_res = {"resistances": [] , "supports": []}

    for index,row in df.iterrows():

        for side in ["resistances","supports"]:

            h_l = "high" if side == "resistances" else "low"


            if row["rounded_" + h_l] in price_group[side]:

                grp = price_group[side][row["rounded_" + h_l]]

                if index>= grp["last"] + min_diff_point*candle_leg:

                    grp["price"].append(row[h_l])

                    if len(grp["price"])>= min_point:

                        extrem_price = max(grp["price"]) if side == "resistances" else mix(grp["price"])

                        support_res[side].append({"price":extrem_price, "broken":False})

                    grp["last"] = index

            else:
                price_group[side][row["rounded_" + h_l]] = {"price":[row[ h_l]] , "start_time":index,"last":index}
                





    


    