import requests
import json
import time
#Die Authentifizierung wird im lokalen Netzwerk noch nicht benötigt, aber im nächsten Schritt
#from requests.auth import HTTPBasicAuth
 
my_hum_url = 'http://openhabian:8080/rest/items/ZWave_Node_003_Sensor_relative_humidity'
my_temp_url = 'http://openhabian:8080/rest/items/ZWave_Node_003_Sensor_temperature'
 
#my_hum_url='http://192.168.68.112:8080/rest/items/ZWaveNode019WohnzimmerZW100Multisensor6_Sensorrelativehumidity'
#my_temp_url='http://192.168.68.112:8080/rest/items/ZWaveNode019WohnzimmerZW100Multisensor6_Sensortemperature'
 
hum_value=requests.get(my_hum_url)
temp_value=requests.get(my_temp_url)
# Das JSON-Objekt wird über die Ausgabe der Requests-Objekt übergeben
 
print(hum_value.content)
print(temp_value.content)
 
#TESTSTRING - AUSGEBEN
temp_dict=json.loads(temp_value.content)
act_temp = temp_dict['state']
act_temp = float(act_temp[:-2])
print(act_temp)
print(type(act_temp))
 
import sqlite3
import time
#cnx = sqlite3.connect(':memory:') alternative in memory database
sqlite_db = 'a_sensor_values.db' # String for creating DB in specified directory
print(sqlite_db)
 
conn=sqlite3.connect(sqlite_db) # Creates sqlite Database - check in your file explorer
cur=conn.cursor()
cur.execute('''DROP TABLE IF EXISTS sensor_values''')
cur.execute('''CREATE TABLE sensor_values(timestamp NUMERIC,temperature NUMERIC, humidity NUMERIC);''') # Create table with specified name and columns/attributes
#
 
for my_counter in range(15):
    time.sleep(60)
    my_timestamp = round(time.time())
    hum_value=requests.get(my_hum_url)
    temp_value=requests.get(my_temp_url)
    hum_dict=json.loads(hum_value.content)
    act_hum = hum_dict['state']
    temp_dict=json.loads(temp_value.content)
    act_temp = temp_dict['state']
    act_temp = float(act_temp[:-2])
     # The temperature value is stored without the "C" in the end.
     # The temperature value is in degrees centi-degrees.
 
   
# CREATE INSERT STATEMENT
    execution_string = f"INSERT INTO sensor_values VALUES ({my_timestamp}, {act_temp}, {act_hum})"
    print(execution_string)
    cur.execute(execution_string)
    conn.commit()
 
import pandas as pd
# retrieve values via pd library from local database
pd.read_sql("SELECT * FROM sensor_values;", conn)
 
import matplotlib.pyplot as plt
import datetime
plot_df=pd.read_sql("SELECT * FROM sensor_values;", conn)
 
timestamps=[]
for i,row in plot_df.iterrows():
   print(row)
   first_time= plot_df.iloc[0]['timestamp']
   second_time= plot_df.iloc[i]['timestamp']  
   duration =  int(second_time - first_time)
   calc_seconds=str(datetime.timedelta(seconds=duration))
   print(calc_seconds)
   timestamps.append(calc_seconds)
 
 
# Create the chart
fig, ax1 = plt.subplots()
ax1.set_title('Temperature vs. Humidity')
color = 'tab:red'
ax1.set_xlabel('Unix Time (Minutes)')
ax1.set_ylabel('Temperature', color=color)
ax1.plot(timestamps,plot_df['temperature'], color=color)
ax1.tick_params(axis='y', labelcolor=color) # changes style and color of y-axis label
ax1.tick_params(axis='x', labelrotation=45)
# Create another line for the Humidity
 
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
 
color = 'tab:blue'
ax2.set_ylabel('Humidity', color=color)  # we already handled the x-label with ax1
ax2.plot(timestamps,plot_df['humidity'], color=color)
ax2.tick_params(axis='y', labelcolor=color)
 
fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.legend(['Temperature'], loc='upper left')
ax2.legend(['Humidity'], loc='upper right')
 
plt.show()
 
#Write to Excel Sheet
#%pip install openpyxl
#import openpype.pipeline as pypeline  # pip install openpype.pipeline to install openpype.pipeline. For windows
 
plot_df=pd.read_sql("SELECT * FROM sensor_values;", conn)
df=plot_df.to_excel('05b_plotting.xlsx')    