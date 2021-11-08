# Maura Toner
# DS 3002 ETL data processor: Project 1

My project ingests two csv files, merges them together on a common id, adds columns using real time API weather data, and then converts to a SQL database table using SQLite.
The project takes a command line variable, which is the filepath to a sqlite3 database. Example of command line and same database output are below.

![Screen Shot 2021-11-07 at 8 25 11 PM](https://user-images.githubusercontent.com/57843918/140674080-2dcdfb89-9cef-4d2f-bc14-df387df767fa.png)
![Screen Shot 2021-11-07 at 8 54 30 PM](https://user-images.githubusercontent.com/57843918/140674085-4acfc696-65ce-401b-a205-fc7bf3acbf1c.png)

My data came from Kaggle, using Movehub rankings for 216 cities in the world. I then used the Open Weather Map API to append real time temperature and weather decription to the data. This updated data was then converted to a SQL database table using SQLite3 in python.

Sources:
   SQLite3 content from UVA DS2001: https://github.com/UVADS/ds2001/blob/main/lecture_notes/python/interacting_w_relational_database.py
   
   Data: https://www.kaggle.com/blitzr/movehub-city-rankings?select=movehubqualityoflife.csv
   
   Sample Weather API call: https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    https://stackoverflow.com/questions/14994948/iterate-each-row-om-table-and-make-api-call
    
  Writing errors and exceptions:
    https://www.programiz.com/python-programming/user-defined-exception
    https://stackoverflow.com/questions/20844347/how-would-i-make-a-custom-error-message-in-python
    
  Sources with SQLite:
    https://datatofish.com/create-database-python-using-sqlite3/
    https://towardsdatascience.com/python-pandas-and-sqlite-a0e2c052456f
    https://stackoverflow.com/questions/2440147/how-to-check-the-existence-of-a-row-in-sqlite-with-python
