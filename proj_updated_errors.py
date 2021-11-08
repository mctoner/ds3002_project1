#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 15:32:05 2021

@author: mauratoner
"""

import pandas as pd
import numpy as np
import requests
import sqlite3
import sys

## NOTE: SEE README for execution and output via command line 


## FETCH DATA
cost = pd.read_csv("https://raw.githubusercontent.com/mctoner/ds3002_project1/main/movehubcostofliving.csv") #reading in link, actual csv file from kaggle and linked in github
cost.head() #table with various costs of living for cities
quality = pd.read_csv("https://raw.githubusercontent.com/mctoner/ds3002_project1/main/movehubqualityoflife.csv")
quality.head() #table of quality of life metrics by city

## MODIFY NUMBER OF COLUMNS
# combine cost and quality tables by common attribute 'city'
df=quality.merge(cost, how='inner', on='City') #concat two data sources together
# (below) use OpenWeather API to create a column for current weather in each city
base_url = "http://api.openweathermap.org/data/2.5/weather?" #API url
api_key = "bc4c03efd67ea7c13afad5ec517ac952" #my personal API key
temps=[] #empty list for storing city temperatures
descriptions=[]
## I will now call the Open Weather Map API to add the current temp and description of weather for each city in the dataaset.
## Note that the API can only call one city at a time with a free subscription, so I looped through the data to make multiple API calls.
for i in range(len(df)): #loop through each city
    city_name = df["City"][i] #call for one city name
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name #complete url for api call includes key and city code
    response = requests.get(complete_url)# return response object
    response.raise_for_status() #raise for status if not 2xx type response 
    x = response.json() #convert data from API call into a JSON
    if x["cod"] != "404": #if not empty or error
        current_temperature = x["main"]["temp"] #store current temperature
        description = x["weather"][0]["description"] #store description of weather
        temps.append(current_temperature) #append current temperature to running list of city temps
        descriptions.append(description)  #append city weather description to running list 
    else:
        sys.exit("City Not Found") #if city not in API data, raise error
df['current_temp_kelvin']=temps #add temperatures as a column to data frame
df['descriptions']=descriptions #add to column in data frame

#  my path_to_db = "/Users/mauratoner/sqlite/ds3002proj.db" -- want to make this a command line variable 
try:
   path_to_db=sys.argv[1] #command line variable will be the path to a sqlite database
   conn = sqlite3.connect(path_to_db)# create database connection and create database if it doesn't already exist
except: #raises error if filepath doesn't exist
    sys.exit('File path incorrect or empty! Supply a CL file path into a database in your SQLite directory') 
cur = conn.cursor() #create cursor

records = df.to_records(index=False) #convert dataframe to list of tuples, necessary to be compatible with SQLite format
result = list(records) #list of tuples to be used by cursor

# create a table in the db called "cities" and pass a schema
cur.execute('drop table if exists cities') #drop table if it exists so we can create new data
conn.commit() #end transaction with commit 

#create table with same column names as df
cur.execute('create table cities (city text,rating real,purchase_power real,healthcare real,pollution real,qualityoflife real,crimerating real,cappucino real,cinema real,wine real,gasoline real,avgrent real,disposable_income real,temp real,description text)')
conn.commit() #commit the changes
# insert multiple records of data with executemany()
cur.executemany('insert into cities values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', result) #insert data from df
conn.commit() #commit the changes

#lastly, check that table was created and data was entered by querying the SQLdatabase
cur.execute("select * from cities") #select all rows and cols from table cities
data=cur.fetchall() #store data in 'data'
# print(data)
if len(data)==0: #if data is empty, table was not created in sqlite successfully
     sys.exit('Error: Table was not successfully made in SQLite!') #raise error for incomplete creation of table
else: #print number of rows and columns of output data
    print("Task completed! A csv of cities has been edited and written to SQL database.", '\nrows=',len(df),'\ncolumns=',len(df.columns))
    
#close cursor and database connection
cur.close()
conn.close()

"""
Sources:
    https://github.com/UVADS/ds2001/blob/main/lecture_notes/python/interacting_w_relational_database.py
    https://www.kaggle.com/blitzr/movehub-city-rankings?select=movehubqualityoflife.csv
    https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    https://stackoverflow.com/questions/14994948/iterate-each-row-om-table-and-make-api-call
    https://www.programiz.com/python-programming/user-defined-exception
    https://stackoverflow.com/questions/20844347/how-would-i-make-a-custom-error-message-in-python
    https://datatofish.com/create-database-python-using-sqlite3/
    https://towardsdatascience.com/python-pandas-and-sqlite-a0e2c052456f
    https://stackoverflow.com/questions/2440147/how-to-check-the-existence-of-a-row-in-sqlite-with-python
    """
    
