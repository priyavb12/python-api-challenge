#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# 
# ---
# 
# ## Starter Code to Generate Random Geographic Coordinates and a List of Cities

# In[41]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress

# Impor the OpenWeatherMap API key
from api_keys import weather_api_key

# Import citipy to determine the cities based on latitude and longitude
from citipy import citipy


# ### Generate the Cities List by Using the `citipy` Library

# In[46]:


# Empty list for holding the latitude and longitude combinations
lat_lngs = []

# Empty list for holding the cities names
cities = []

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name

    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(f"Number of cities in the list: {len(cities)}")


# In[48]:


cities


# ---

# ## Requirement 1: Create Plots to Showcase the Relationship Between Weather Variables and Latitude
# 
# ### Use the OpenWeatherMap API to retrieve weather data from the cities list generated in the started code

# In[52]:


url = f"http://api.openweathermap.org/data/2.5/weather?units=metric&appid={weather_api_key}"
print(url +'&q=san francisco')


# In[54]:


# Set the API base URL
url = f"http://api.openweathermap.org/data/2.5/weather?units=metric&appid={weather_api_key}"

# Define an empty list to fetch the weather data for each city
city_data = []

# Print to logger
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters
record_count = 1
set_count = 1

# Loop through all the cities in our list to fetch weather data
for i, city in enumerate(cities):

    # Group cities in sets of 50 for logging purposes
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 0

    # Create endpoint URL with each city
    city_url = f"{url}&q={city}"

    # Log the url, record, and set numbers
    print("Processing Record %s of Set %s | %s" % (record_count, set_count, city))

    # Add 1 to the record count
    record_count += 1

    # Run an API request for each of the cities
    try:
        # Parse the JSON and retrieve data
        city_weather = requests.get(city_url).json()

        # Parse out latitude, longitude, max temp, humidity, cloudiness, wind speed, country, and date
        city_lat = city_weather['coord']['lat']
        city_lng = city_weather['coord']['lon']
        city_max_temp = city_weather['main']['temp_max']
        city_humidity = city_weather['main']['humidity']
        city_clouds = city_weather['clouds']['all']
        city_wind = city_weather['wind']['speed']
        city_country = city_weather['sys']['country']
        city_date = city_weather['dt']

        # Append the City information into city_data list
        city_data.append({"City": city,
                          "Lat": city_lat,
                          "Lng": city_lng,
                          "Max Temp": city_max_temp,
                          "Humidity": city_humidity,
                          "Cloudiness": city_clouds,
                          "Wind Speed": city_wind,
                          "Country": city_country,
                          "Date": city_date})

    # If an error is experienced, skip the city
    except:
        print("City not found. Skipping...")
        pass

    # pause to avoid rate limiting
    #time.sleep(1)

# Indicate that Data Loading is complete
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")


# In[56]:


# Convert the cities weather data into a Pandas DataFrame
city_data_df = pd.DataFrame(city_data)

# Show Record Count
city_data_df.count()


# In[58]:


# Display sample data
city_data_df.head()


# In[60]:


# Export the City_Data into a csv
city_data_df.to_csv("output_data/cities.csv", index_label="City_ID")


# In[62]:


# Read saved data
city_data_df = pd.read_csv("output_data/cities.csv", index_col="City_ID")

# Display sample data
city_data_df.head()


# ### Create the Scatter Plots Requested
# 
# #### Latitude Vs. Temperature

# In[65]:


import time

# Build scatter plot for latitude vs. temperature


plt.scatter(city_data_df['Lat'],
           city_data_df['Max Temp'],edgecolor='r',
            linewidth=1,
            marker='o',
            alpha=0.8,label='cities')

# Incorporate the other graph properties
date = time.strftime('%y-%m-%d')

plt.title(f"city max latitude vs temperature (%s) ({date})")
plt.xlabel('Latitude')
plt.ylabel('Max Temp(C)')


# Save the figure
plt.savefig("output_data/Fig1.png")

# Show plot
plt.show()


# #### Latitude Vs. Humidity

# In[68]:


# Build the scatter plots for latitude vs. humidity
plt.scatter(city_data_df['Lat'],
           city_data_df['Humidity'],edgecolor='orange',
            linewidth=1,
            marker='o',
            alpha=0.8,label='cities')

# Incorporate the other graph properties
date = time.strftime('%y-%m-%d')

plt.title(f"city max latitude vs Humididty ({date})")
plt.xlabel('Latitude')
plt.ylabel('humidity(%)')


# Save the figure
plt.savefig("output_data/Fig2.png")

# Show plot
plt.show()


# #### Latitude Vs. Cloudiness

# In[71]:


# Build the scatter plots for latitude vs. cloudiness
plt.scatter(city_data_df['Lat'],
           city_data_df['Cloudiness'],edgecolor='blue',
            linewidth=1,
            marker='o',
            alpha=0.8,label='cities')

# Incorporate the other graph properties
date = time.strftime('%y-%m-%d')

plt.title(f"city max latitude vs Cloudiness ({date})")
plt.xlabel('Latitude')
plt.ylabel('Cloudiness(%)')

# Save the figure
plt.savefig("output_data/Fig3.png")

# Show plot
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[74]:


# Build the scatter plots for latitude vs. wind speed
plt.scatter(city_data_df['Lat'],
           city_data_df['Wind Speed'],edgecolor='green',
            linewidth=1,
            marker='o',
            alpha=0.8,label='cities')


# Incorporate the other graph properties
date = time.strftime('%y-%m-%d')

plt.title(f"city max latitude vs Wind Speed ({date})")
plt.xlabel('Latitude')
plt.ylabel('Wind Speed(%)')


# Save the figure
plt.savefig("output_data/Fig4.png")

# Show plot
plt.show()


# ---
# 
# ## Requirement 2: Compute Linear Regression for Each Relationship
# 

# In[77]:


# Define a function to create Linear Regression plots
def plot_linear_regression(x_value, y_value, title, text_coord):

    (slope, intercept, rvalue, pvalue, stderr) = linregress(x_value, y_value)
    regress_value = x_value * slope + intercept
    line_eq = f"y = {round(slope,2)}x +{round(intercept,2)}"

    plt.scatter(x_value,y_value)
    plt.plot(x_value, regress_value, 'r-')
    plt.annotate(line_eq, text_coord, fontsize=15, color = 'r')
    plt.xlabel('lat')
    plt.ylabel(title)
    print(f"The r-value is {rvalue ** 2}")
    plt.show()


# In[79]:


# Create a DataFrame with the Northern Hemisphere data (Latitude >= 0)
# YOUR CODE HERE
northern_hemi_df = city_data_df[city_data_df['Lat']>=0]
# Display sample data
northern_hemi_df.head()


# In[81]:


# Create a DataFrame with the Southern Hemisphere data (Latitude < 0)
# YOUR CODE HERE
southern_hemi_df = city_data_df[city_data_df['Lat']<0]
# Display sample data
southern_hemi_df.head()


# ###  Temperature vs. Latitude Linear Regression Plot

# In[84]:


# Linear regression on Northern Hemisphere
# YOUR CODE HERE

x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Max Temp']
plot_linear_regression(x_values, y_values, 'Max Temp', (6, -10))


# In[86]:


# Linear regression on Southern Hemisphere
# YOUR CODE HERE

x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Max Temp']
plot_linear_regression(x_values, y_values, 'Max Temp',(-55, 5))


# **Discussion about the linear relationship:** YOUR RESPONSE HERE

# ### Humidity vs. Latitude Linear Regression Plot

# In[90]:


# Northern Hemisphere
# YOUR CODE HERE
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Humidity']
plot_linear_regression(x_values, y_values, 'Humidity',(6, -10))


# In[92]:


# Southern Hemisphere
# YOUR CODE HERE
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Max Temp']
plot_linear_regression(x_values, y_values, 'Max Temp',(-55, 5))


# **Discussion about the linear relationship:** YOUR RESPONSE HERE

# ### Cloudiness vs. Latitude Linear Regression Plot

# In[96]:


# Northern Hemisphere
# YOUR CODE HERE

x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Humidity']
plot_linear_regression(x_values, y_values, 'Humidity',(6, -10))


# In[98]:


# Southern Hemisphere
# YOUR CODE HERE
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Max Temp']
plot_linear_regression(x_values, y_values, 'Max Temp',(-55, 5))


# **Discussion about the linear relationship:** YOUR RESPONSE HERE

# ### Wind Speed vs. Latitude Linear Regression Plot

# In[102]:


# Northern Hemisphere
# YOUR CODE HERE
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Humidity']
plot_linear_regression(x_values, y_values, 'Humidity',(6, -10))


# In[104]:


# Southern Hemisphere
# YOUR CODE HERE

x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Max Temp']
plot_linear_regression(x_values, y_values, 'Max Temp',(-55, 5))


# **Discussion about the linear relationship:** YOUR RESPONSE HERE

# In[ ]:


The Python API Challenge WeatherPy part discusses linear relationships by computing linear regression for 
various weather parameters and latitudes across the Northern and Southern Hemispheres.
As part of this process, scatter plots are created for different pairs of variables, such as temperature,
humidity, cloudiness, and wind speed against latitude. An analysis of linear regression is helpful in understanding 
the relationship between weather parameters and latitude in each hemisphere.
We aim to visualize and interpret how these parameters change as one moves closer to or farther from the equator.

