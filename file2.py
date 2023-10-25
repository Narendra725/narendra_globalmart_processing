import pandas as pd

data=pd.read_json("22d13816-59fd-44d1-97dc-c98af92c480c_83d04ac6-cb74-4a96-a06a-e0d5442aa126_globalmart_data_from_0th_offset.json")

## Question 1:month wise sales amt report
from datetime import datetime as dt
data["order_date"]=pd.to_datetime(data["order"].apply(lambda x : x["order_purchase_date"]))
data["month"]=data["order_date"].apply(lambda x: x.strftime("%B"))
print(data.pivot_table(index="month",values="sales_amt",aggfunc="sum").sort_values(by= "sales_amt",ascending=False).reset_index())

#Question 2:Month wise profit_amount report
data["profit_amt"][data["profit_amt"]=="null"]=0
print(data.pivot_table(index="month",values="profit_amt",aggfunc="sum").sort_values(by= "profit_amt",ascending=False).reset_index())

#Question 3: Number of months whose overall profit is positive
res=data.pivot_table(index="month",values="profit_amt",aggfunc="sum").sort_values(by= "profit_amt",ascending=False).reset_index()
print(len(res[res["profit_amt"]>0]))

#Quesion 4 : Number of late deliveries
data["del_date"]=data["order"].apply(lambda x: x["order_delivered_customer_date"])
data["exp_del_date"]=data["order"].apply(lambda x: x["order_estimated_delivery_date"])
data=data[data["del_date"] != 'null']
data=data[data["exp_del_date"] != 'null']
data["del_date"]=pd.to_datetime(data["del_date"])
data["exp_del_date"]=pd.to_datetime(data["exp_del_date"])
data["late_dur"]=data["exp_del_date"]-data["del_date"]
data["late_dur"]=data["late_dur"].apply(lambda x :x.days)
print(len(data[data["late_dur"] < 0]))

# Question 5: Vendor wise late deliveries report
data["vendor"]=data["order"].apply(lambda x : x["vendor"]["VendorID"])
data["is_late"]=data["late_dur"].apply(lambda x : 1 if x<0 else 0)
print(data.pivot_table(index="vendor",values="is_late",aggfunc="sum").sort_values(by= "is_late",ascending=False).reset_index())
