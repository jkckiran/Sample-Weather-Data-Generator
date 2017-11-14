# Sample-Weather-Data-Generator

## This repository contains the following python codes which will generate sample weather data using machine learning algorithms.

* Test_Weather_v3.py - This is the master script which invokes other python scripts for execution.
* location_data.py - This script fetches location data such as latitude, longitude, elevation co-ordinates for the given set of train locations in the input file.
* weather_data.py - This script fetches weather data such as temperature, pressure, humidity, etc... by taking the location co-ordinates (created in previous script) as input.
* model_data.py - This script creates 4 learning models for each response variable (temperature, pressure, humidity, conditions).
* weather_prediction.py - This script will predict the output values for the given set of test locations using the models that are already trained based on training data.



**Input File 1** - train_file.txt contains the list of locations that have been used to train the machine learning models.

**Input File 2** - test_file.txt contains the list of locations for which the weather details have been predicted / generated using the machine learning models that were trained before.

**Output File** - output_weather_info.psv is a pipe separated file containing the predicted / generated weather data for the test locations

*Intermediate File* - train_weather_data.csv is an intermediate file (just for reference) created from a Dataframe which is used to train the models for prediction.

*Error Logs* - error_log.txt is a text file used to contain error records, if any.

## Dependencies / Packages
This program requires Python-3.x and following Python Packages

* pandas (To create and process Dataframes)
* sklearn (To create and train machine learning models)
* numpy (To predict using machine learning models)
* forecastio (To download weather data for the given list of locations)

## Dependencies / Packages Installation
```
pip install pandas
pip install sklearn
pip install numpy
pip install python-forecastio
```
**Note : Please use "sudo" if there is no access to install the packages in the Linux environment**

## Execution Method
Open Command Prompt / Terminal ---> *path_to_python.exe\python path_to_python_file\python_file.py*

Tested in Windows environment

**Example 1 - python Test_Weather.py**

**Example 2 - C:\Users\user_name\Anaconda3\python C:\Users\user_name\Test_Weather.py**
