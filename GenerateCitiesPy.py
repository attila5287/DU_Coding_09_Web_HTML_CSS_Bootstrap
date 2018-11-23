# Project Objective:
# build a series of scatter plots to showcase the following relationships via random cities/geo-coords:
import warnings
from citipy import citipy
import time
import api_keys
import urllib
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')
# previously created csv file
csv_path = 'output_data/cities_v2.csv'
print("Review results on csv file with path: " + csv_path)

# Randomly select at least 500 unique (non-repeat) cities based on latitude and longitude.
rand_lats = list(np.random.uniform(high=-90.00, low=90.00, size=150))
rand_longs = list(np.random.uniform(high=-90.00, low=90.00, size=150))
print("Test Size: "+str(len(rand_lats))+" latitudes and " +
      str(len(rand_longs)) + " longitudes generated...")

# citipy module to pull nearest city name by lat/long

rand_city = []
for lat, long in zip(rand_lats, rand_longs):
    city = citipy.nearest_city(lat, long).city_name
#     print("(lat: %s, long: %s) -> %s"  %(lat,long,city))
    if city not in rand_city:
        rand_city.append(city)
len_rand_city = len(rand_city)
print("Total of %s random cities retrived via random lat/long pairs" %
      (len_rand_city))
print("First five random and unique cities: ")
print(rand_city[0:5])

# Print the city count to confirm sufficient count
city_count = len(rand_city)
if city_count >= 500:
    print(str(city_count) + " cities: sufficient")
else:
    print(str(city_count) +
          " cities randomly generated: insufficient...\n\t*** Test run only! ***")

# perform a weather check on each of the cities using a series of successive API calls.

# OW api key imported from api.py module created for this purpose within the same folder of JNbk
api_key = api_keys.api_key
# base url that will be used during the iteration by adding city at the end
url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + api_key
city_data = []
# Include a print log of each city as it's being processed with the city number and city name:

print("---------Processing: Real-Time Weather Data %s ---------" %
      time.strftime("%x"))
for city in rand_city:
    print("City weather records: requesting %s of %s | %s" %
          (rand_city.index(city)+1, city_count+1, city))
# urllib for city names with multiple words/parsing error: mayor pablo lagerenza/ mayor%20pablo%20lagerenza
    city_url = url + "&q=" + urllib.request.pathname2url(city)
    print(city_url)
    try:
        openweather = requests.get(city_url).json()
        # Append the City information into city_data list
        city_data.append({"City": city,
                          "Lat": openweather["coord"]["lat"],
                          "Lng": openweather["coord"]["lon"],
                          "Max Temp": openweather["main"]["temp_max"],
                          "Humidity": openweather["main"]["humidity"],
                          "Cloudiness": openweather["clouds"]["all"],
                          "Wind Speed": openweather["wind"]["speed"],
                          "Country": openweather["sys"]["country"],
                          "Date": openweather["dt"]})
    # If an error is experienced, skip the city
    except:
        print("No records returned from request")
        pass

print("---------Completed: Real-Time Weather Data %s ---------" %
      time.strftime("%x"))


# Convert array of JSONs into Pandas DataFrame
mastercity_df = pd.DataFrame(city_data)
mastercity_df.head(10)
# mastercity_df.count()

# Save both a CSV of all data retrieved and png images for each scatter plot.
mastercity_df.to_csv(csv_path, index_label="City_ID")

# confirm unique cities for city record count
final_citycount = len(mastercity_df['City'])
print("Completed records for %s out of %s randomly generated cities: sufficient" %
      (final_citycount, len(rand_city)))
if final_citycount < 500:
    print('\ninsufficient...\n\t*** Test run? ***')

# build a series of scatter plots for following
# [1] Temperature (F) vs. Latitude
# [2] Humidity (% ) vs. Latitude
# [3] Cloudiness (%) vs. Latitude
# [4] Wind Speed (mph) vs. Latitude

# copy dataframe with four columns required for plot iteration
renamedforplot_df = mastercity_df.filter(
    ['Max Temp', 'Humidity', 'Cloudiness', 'Wind Speed'], axis=1)
# rename columns of above created dataframe per assignment instructions
renamedforplot_df = renamedforplot_df.rename(columns={'Max Temp': 'Temperature (F)',
                                                      'Humidity': ' Humidity (%)',
                                                      'Cloudiness': 'Cloudiness (%)',
                                                      'Wind Speed': 'Wind Speed (mph)'})
# create a color list for iteration creating plots
color_list = ['b',  'c', 'm', 'y']
size = 100
ax_list = renamedforplot_df.columns
ax_list

# scatter plots with todays date, then save on output_data output_data folder and print messages along
for axis, color in zip(ax_list, color_list):
    plt.figure(figsize=(15, 6))
    plt.title(axis + " vs Lattitude (%s)" % time.strftime("%x"))
    plt.scatter(mastercity_df['Lat'], renamedforplot_df[axis], s=size,
                marker="o", facecolors=color, edgecolors="black", alpha=0.90)
    plt.xlabel('Latitude')
    plt.ylabel(axis)
    plt.grid(True)
    plt.savefig('output_data/v2_Lattitude_vs_'+axis)
    plt.show()
    print("\t* " + axis + " vs Lat. saved as ..." +
          'output_data/Lattitude_vs_'+axis+".png")
    print("\n")


mastercity_df['Date_'] = dt.mastercity_df['Date']
