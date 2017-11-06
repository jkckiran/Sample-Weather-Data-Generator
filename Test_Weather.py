# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 20:08:35 2017

@author: Kiran Chandar Jayaraman
"""
# import necessary packages required for processing
import datetime
import requests
import pandas as pd
import forecastio
import numpy as np

# Importing Supervised Learning Estimators. 
# Linear Regression for Numeric variables & Naive Bayes for String variables
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
#------------------------------------------------------------------------------
# This function takes a list of locations as input.
# Generates Location Details for training or testing the model.
# Error file will be created containing the locations for which the data are not available
def fetch_location_info(input_list):
    
    LatLong_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    Elevation_URL = 'https://maps.googleapis.com/maps/api/elevation/json?locations='
    
    # Initializing Error Logs with relevant title for writing error records
    err_line_header = "Logging Location Data Errors"
    print(err_line_header, file=err_file)
    for i in range(len(err_line_header)):
        print("-", end='', file=err_file)
    print("\n", file=err_file)
    # Fetch and Extract Location details from google maps
    input_info = []
    
    for location in input_list:
        temp_info = {'Location': location}
        latlong_response = requests.get(LatLong_URL+location).json()
        if latlong_response.get('results'):
            for latlong_results in latlong_response.get('results'):
                latlong = latlong_results.get('geometry','0').get('location','0')
                temp_info['Latitude'] = latlong.get('lat','0')
                temp_info['Longitude'] = latlong.get('lng','0')
                
                elevation_response = requests.get(Elevation_URL + str(temp_info['Latitude']) + ',' + str(temp_info['Longitude'])).json()                
                if elevation_response.get('results'):
                    for elevation_results in elevation_response.get('results'):
                        temp_info['Elevation'] = elevation_results.get('elevation', '0')
                        input_info.append(temp_info) 
                        break
                else:
                    print("Elevation_URL is not fetching Elevation values for {}".format(location), file=err_file)                
                
                break                
        else:
            print("LatLong_URL is not fetching Latitude, Longitude values for {}".format(location), file=err_file)
    
    print("\n", file=err_file)
    return input_info
#------------------------------------------------------------------------------
# This function generates weather related details for a particular location
# Input - List of locations with co-ordinates, start_date and the forecast.io api_key
# Output - A dictionary file containing weather related details for a particular location
def fetch_weather_info(train_input_info, start_date, api_key):
    weather_info = {}
    
    for temp_info in train_input_info:
        for date_offset in range(0, 180, 7):
            forecast = forecastio.load_forecast(
                api_key,
                temp_info['Latitude'],
                temp_info['Longitude'],
                time=start_date+datetime.timedelta(date_offset),
                units="us"
            )
            
            # Temperature is not available in daily().data.
            # So fetch hourly().data to extract temperature values for a particular location
            for hour in forecast.hourly().data:
                
                weather_info['Location'] = weather_info.get('Location', []) + [temp_info['Location']]
                weather_info['Latitude'] = weather_info.get('Latitude', []) + [temp_info['Latitude']]
                weather_info['Longitude'] = weather_info.get('Longitude', []) + [temp_info['Longitude']]
                weather_info['Elevation'] = weather_info.get('Elevation', []) + [temp_info['Elevation']]
                weather_info['Conditions'] = weather_info.get('Conditions', []) + [hour.d.get('summary', '')]
                weather_info['Temperature'] = weather_info.get('Temperature', []) + [hour.d.get('temperature', 75)]
                weather_info['Humidity'] = weather_info.get('Humidity', []) + [hour.d.get('humidity', 0.5)]
                weather_info['Pressure'] = weather_info.get('Pressure', []) + [hour.d.get('pressure', 1000)]
                weather_info['Time'] = weather_info.get('Time', []) + [hour.d['time']]                  
    
    return weather_info    
#------------------------------------------------------------------------------
# This function takes the dataframe with location and weather details as input train data.
# It trains respective models based on input train data
# And create models to predict temperature, pressure, humidity and conditions for the testing locations
# The Independent Variable 'x' is the combination of lat, long and elev
# The Dependent Variable 'y' differs for each model
def train_model(df):

    x = df[['Latitude', 'Longitude', 'Elevation']].values
    
    # Train the Linear Regression model for "Temperature" variable
    train_temperature = LinearRegression()
    y = df[['Temperature']].values
    train_temperature.fit(x, y)
    
    # Train the Linear Regression model for "Pressure" variable
    train_pressure = LinearRegression()
    y = df[['Pressure']].values
    train_pressure.fit(x, y)
    
    # Train the Linear Regression model for "Humidity" variable
    train_humidity = LinearRegression()
    y = df[['Humidity']].values
    train_humidity.fit(x, y)
    
    # Train the Gaussian Naive Bayes model for "Conditions" variable
    train_conditions = GaussianNB()
    y = df[['Conditions']].values.ravel()
    train_conditions.fit(x, y)

    return train_temperature, train_pressure, train_humidity, train_conditions
#------------------------------------------------------------------------------
# This function will predict necessary variables based on respective trained models.
# Input - Testing Location Data along with machine learning models to predict the results.
# Output - A dictionary with the required variables predicted by the models.
def predict_weather_info(test_input_info, train_temperature, train_pressure, train_humidity, train_conditions, start_date):

    weather_data = {}

    for temp_info in test_input_info:
        
        # Splitting and fetching only the city part of "Location" variable.
        loc = temp_info['Location']
        loc = loc.split(',')[0]
        
        # Formatting the floating variables to limit the decimal points to two.
        lat = float("{0:.2f}".format(temp_info['Latitude']))
        lng = float("{0:.2f}".format(temp_info['Longitude']))
        elev = float("{0:.2f}".format(temp_info['Elevation']))
        
        for date_offset in range(0, 180, 30):
            new_date = start_date + datetime.timedelta(date_offset)

            weather_data['Location'] = weather_data.get('Location', []) + [loc]
            
            # The output "Position" variable is the combination of lat, long and elev values.
            weather_data['Position'] = weather_data.get('Position', []) + [str(lat) + ',' + str(lng) + ',' + str(elev)]
            
            # The output "Local Time" variable is of ISO8601 datetime format
            weather_data['Local Time'] = weather_data.get('Local Time', []) + [new_date.isoformat()]

            # The output "Conditions" variable is predicted using the machine learning model
            cond = train_conditions.predict(np.array([lat, lng, elev]).reshape(1, -1))[0].lower()
            if 'clear' not in cond:
                cond = 'Rain'
            elif 'snow' in cond:
                cond = 'Snow'
            else:
                cond = 'Sunny'
            
            weather_data['Conditions'] = weather_data.get('Conditions', []) + [cond]
            
            # The output "Temperature" variable is predicted using the machine learning model
            # The default Fahrenheit value is then converted into Celsius.
            temp = train_temperature.predict(np.array([lat, lng, elev]).reshape(1, -1))[0][0]
            temp_celsius = (5.0 / 9.0)*(temp - 32)
            weather_data['Temperature'] = weather_data.get('Temperature', []) + [temp_celsius]

            # The output "Pressure" variable is predicted using the machine learning model
            pres = train_pressure.predict(np.array([lat, lng, elev]).reshape(1, -1))[0][0]
            weather_data['Pressure'] = weather_data.get('Pressure', []) + [pres]

            # The output "Humidity" variable is predicted using the machine learning model
            hum = train_humidity.predict(np.array([lat, lng, elev]).reshape(1, -1))[0]
            weather_data['Humidity'] = weather_data.get('Humidity', []) + [int(hum * 100)]

    return weather_data
#------------------------------------------------------------------------------
# Main Function which inturn invokes other functions for generating weather data.
if __name__ == '__main__':

    # List of locations for fetching weather data to train the model
    input_train_list = None
    with open('data/train_file.txt') as input:
        input_train_list = [line.strip() for line in input]
    
    # Opening error file for logging errors, if any
    err_file = open('data/error_log.txt', 'w')
    
    # Fetching location co-ordinates for the list of input Train locations
    train_input_info = fetch_location_info(input_train_list)
    
    # Fetching weather details for a particular location using python's forecast.io package
    train_weather_info = fetch_weather_info(train_input_info, datetime.datetime(2017, 1, 1), '18983ac30d0a7203f001f8d66b2e180b')

    # Converting the extracted weather info details into a Dataframe for later use
    train_weather_df = pd.DataFrame(train_weather_info)
    
    # Writing the intermediate Weather Dataframe into a CSV file for reference
    train_weather_df.to_csv('data/train_weather_data.csv', index=False)
    
    # Generating various models for predicting weather data
    train_temperature, train_pressure, train_humidity, train_conditions = train_model(train_weather_df)
    
    # List of locations to test the model
    input_test_list = None
    with open('data/test_file.txt') as input:
        input_test_list = [line.strip() for line in input]
    
    # Fetching location co-ordinates for the list of input Test locations
    test_input_info = fetch_location_info(input_test_list)

    # Date from which we will start predicting data every single day for 30 days 
    start_date = datetime.datetime(2017, 6, 1)
    
    # Predicting weather data by using trained machine learning models
    test_weather_info = predict_weather_info(test_input_info, train_temperature, train_pressure, train_humidity, train_conditions, start_date)
    
    # Generating output dataframe so that we can write it in the file
    test_weather_df = pd.DataFrame(test_weather_info)
    
    # Create pipe-separated output file along with header
    test_weather_df[["Location", "Position", "Local Time", "Conditions", "Temperature", "Pressure", "Humidity"]].to_csv(
        "data/output_weather_info.psv",
        header=True,
        index=False,
        sep='|'
    )    
    
    err_file.close()
#------------------------------------------------------------------------------    