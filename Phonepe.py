import os
import pandas as pd
import json
import mysql.connector


#Aggregated_Transaction data
Agg_trans_path="C:/Users/WELCOME/pulse/data/aggregated/transaction/country/india/state/"
Agg_trans_list=os.listdir(Agg_trans_path)
Agg_trans_list

Agg_trans_data={'State':[], 'Year':[], 'Quater':[], 'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

for i in Agg_trans_list:
    p_i=Agg_trans_path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
                Name = z['name']
                count = z['paymentInstruments'][0]['count']
                amount = z['paymentInstruments'][0]['amount']
                Agg_trans_data['Transaction_type'].append(Name)
                Agg_trans_data['Transaction_count'].append(count)
                Agg_trans_data['Transaction_amount'].append(amount)
                Agg_trans_data['State'].append(i)
                Agg_trans_data['Year'].append(j)
                Agg_trans_data['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_trans = pd.DataFrame(Agg_trans_data)

Agg_trans["State"] = Agg_trans["State"].str.replace("-"," ")
Agg_trans["State"] = Agg_trans["State"].str.title()
Agg_trans["State"] = Agg_trans["State"].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

#------------------------------------------------------------------------------


#Aggregated_User data
Agg_user_path="C:/Users/WELCOME/pulse/data/aggregated/user/country/india/state/"
Agg_user_list=os.listdir(Agg_user_path)
Agg_user_list

Agg_user_data = {'State':[], 'Year':[], 'Quater':[], 'Brand':[], 'Count':[], 'Percentage':[]}

for i in Agg_user_list:
    p_i=Agg_user_path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            try:
                for z in D['data']['usersByDevice']:
                    brands = z['brand']
                    counts = z['count']
                    percentages = z['percentage']
                    Agg_user_data['Brand'].append(brands)
                    Agg_user_data['Count'].append(counts)
                    Agg_user_data['Percentage'].append(percentages)
                    Agg_user_data['State'].append(i)
                    Agg_user_data['Year'].append(j)
                    Agg_user_data['Quater'].append(int(k.strip('.json')))
            except:
                pass

Agg_user = pd.DataFrame(Agg_user_data)

Agg_user["State"] = Agg_user["State"].str.replace("-"," ")
Agg_user["State"] = Agg_user["State"].str.title()
Agg_user["State"] = Agg_user["State"].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

#------------------------------------------------------------------------------


#Map_Transaction data
Map_trans_path = "C:/Users/WELCOME/pulse/data/map/transaction/hover/country/india/state/"
Map_trans_list = os.listdir(Map_trans_path)
Map_trans_list

Map_trans_data =  {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [], 'Amount': []}

for i in Map_trans_list:
    p_i=Map_trans_path+i+"/"
    Map_yr=os.listdir(p_i)
    for j in Map_yr:
        p_j=p_i+j+"/"
        Map_yr_list=os.listdir(p_j)
        for k in Map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['hoverDataList']:
                district = z['name']
                count = z["metric"][0]["count"]
                amount = z["metric"][0]["amount"]
                Map_trans_data["District"].append(district)
                Map_trans_data["Count"].append(count)
                Map_trans_data["Amount"].append(amount)
                Map_trans_data['State'].append(i)
                Map_trans_data['Year'].append(j)
                Map_trans_data['Quarter'].append(int(k.strip('.json')))

Map_trans = pd.DataFrame(Map_trans_data)

Map_trans["State"] = Map_trans["State"].str.replace("-"," ")
Map_trans["State"] = Map_trans["State"].str.title()
Map_trans["State"] = Map_trans["State"].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

#------------------------------------------------------------------------------



#Map_User data
Map_user_path = "C:/Users/WELCOME/pulse/data/map/user/hover/country/india/state/"
Map_user_list = os.listdir(Map_user_path)
Map_user_list

Map_user_data = {"State": [], "Year": [], "Quarter": [], "District": [], "RegisteredUser": [], "AppOpens": []}

for i in Map_user_list:
    p_i=Map_user_path+i+"/"
    Map_yr=os.listdir(p_i)
    for j in Map_yr:
        p_j=p_i+j+"/"
        Map_yr_list=os.listdir(p_j)
        for k in Map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']["hoverData"].items():
                district = z[0]
                registereduser = z[1]["registeredUsers"]
                appOpens = z[1]['appOpens']
                Map_user_data["District"].append(district)
                Map_user_data["RegisteredUser"].append(registereduser)
                Map_user_data["AppOpens"].append(appOpens)
                Map_user_data['State'].append(i)
                Map_user_data['Year'].append(j)
                Map_user_data['Quarter'].append(int(k.strip('.json')))

Map_user = pd.DataFrame(Map_user_data)

Map_user["State"] = Map_user["State"].str.replace("-"," ")
Map_user["State"] = Map_user["State"].str.title()
Map_user["State"] = Map_user["State"].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

#------------------------------------------------------------------------------



#Top_Transaction data
Top_trans_path = "C:/Users/WELCOME/pulse/data/top/transaction/country/india/state/"
Top_trans_list = os.listdir(Top_trans_path)
Top_trans_list

Top_trans_data = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [], 'Transaction_amount': []}

for i in Top_trans_list:
    p_i=Top_trans_path+i+"/"
    Top_yr=os.listdir(p_i)
    for j in Top_yr:
        p_j=p_i+j+"/"
        Top_yr_list=os.listdir(p_j)
        for k in Top_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
                name = z['entityName']
                count = z['metric']['count']
                amount = z['metric']['amount']
                Top_trans_data['Pincode'].append(name)
                Top_trans_data['Transaction_count'].append(count)
                Top_trans_data['Transaction_amount'].append(amount)
                Top_trans_data['State'].append(i)
                Top_trans_data['Year'].append(j)
                Top_trans_data['Quarter'].append(int(k.strip('.json')))

Top_trans = pd.DataFrame(Top_trans_data)

Top_trans["State"] = Top_trans["State"].str.replace("-"," ")
Top_trans["State"] = Top_trans["State"].str.title()
Top_trans["State"] = Top_trans["State"].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

#------------------------------------------------------------------------------



#Top_User data
Top_user_path = "C:/Users/WELCOME/pulse/data/top/user/country/india/state/"
Top_user_list = os.listdir(Top_user_path)
Top_user_list

Top_user_data = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'RegisteredUsers': []}

for i in Top_user_list:
    p_i=Top_user_path+i+"/"
    Top_yr=os.listdir(p_i)
    for j in Top_yr:
        p_j=p_i+j+"/"
        Top_yr_list=os.listdir(p_j)
        for k in Top_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
                name = z['name']
                registeredUsers = z['registeredUsers']
                Top_user_data['Pincode'].append(name)
                Top_user_data['RegisteredUsers'].append(registeredUsers)
                Top_user_data['State'].append(i)
                Top_user_data['Year'].append(j)
                Top_user_data['Quarter'].append(int(k.strip('.json')))

Top_user = pd.DataFrame(Top_user_data)

Top_user["State"] = Top_user["State"].str.replace("-"," ")
Top_user["State"] = Top_user["State"].str.title()
Top_user["State"] = Top_user["State"].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

#------------------------------------------------------------------------------

#Creating a Database and Table and inserting the data into sql

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "")
print(mydb)
mycursor = mydb.cursor(buffered = True)

mycursor.execute('create database phonepe_pulse')
mycursor.execute('use phonepe_pulse')

mycursor.execute('create table Agg_Trans (State VARCHAR(50), Year INT(50), Quarter INT(50), Transaction_Type VARCHAR(225), Transaction_Count INT(50), Transaction_Amount FLOAT(50))')
for _,row in Agg_trans.iterrows():
    mycursor.execute("INSERT INTO Agg_Trans VALUES (%s,%s,%s,%s,%s,%s)", tuple(row))
    mydb.commit()

mycursor.execute('create table Agg_User (State VARCHAR(50), Year INT(50), Quarter INT(50), Brands VARCHAR(50), Transaction_Count INT(50), Percentage FLOAT(50))')
for _,row in Agg_user.iterrows():
    mycursor.execute("INSERT INTO Agg_User VALUES (%s,%s,%s,%s,%s,%s)", tuple(row))
    mydb.commit()

mycursor.execute('create table Map_Trans (State VARCHAR(50), Year INT(50), Quarter INT(50), District VARCHAR(50), Transaction_Count INT(50), Transaction_Amount FLOAT(50))')
for _,row in Map_trans.iterrows():
    mycursor.execute("INSERT INTO Map_Trans VALUES (%s,%s,%s,%s,%s,%s)", tuple(row))
    mydb.commit()
    
mycursor.execute('create table Map_User (State VARCHAR(50), Year INT(50), Quarter INT(50), District VARCHAR(50), Registered_User INT(50), App_Opens INT(50))')
for _,row in Map_user.iterrows():
    mycursor.execute("INSERT INTO Map_User VALUES (%s,%s,%s,%s,%s,%s)", tuple(row))
    mydb.commit()

mycursor.execute('create table Top_Trans (State VARCHAR(50), Year INT(50), Quarter INT(50), Pincode INT(50), Transaction_Count INT(50), Transaction_Amount FLOAT(50))')
for _,row in Top_trans.iterrows():
    mycursor.execute("INSERT INTO Top_Trans VALUES (%s,%s,%s,%s,%s,%s)", tuple(row))
    mydb.commit()

mycursor.execute('create table Top_User (State VARCHAR(50), Year INT(50), Quarter INT(50), Pincode INT(50), Registered_Users INT(50))')
for _,row in Top_user.iterrows():
    mycursor.execute("INSERT INTO Top_User VALUES (%s,%s,%s,%s,%s)", tuple(row))
    mydb.commit()

#-----------------------------------------------------------------------------------------------------------------------------------------


