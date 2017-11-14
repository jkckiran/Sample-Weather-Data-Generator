# import necessary packages required for processing
import datetime
import pandas as pd

# Importing functions from other python modules / scripts
from location_data import fetch_location_info
from weather_data import fetch_weather_info
from model_data import train_model
from weather_prediction import predict_weather_info

# Main Function which inturn invokes other functions for creating weather data.


if __name__ == '__main__':

    # List of locations for fetching weather data to train the model
    input_train_list = None
    with open('data/train_file.txt') as input:
        input_train_list = [line.strip() for line in input]

    # Opening error file for logging errors, if any
    err_file = open('data/error_log.txt', 'w')

    # Fetching location co-ordinates for the list of input Train locations
    train_input_info = fetch_location_info(input_train_list, err_file)

    # Fetching weather data for each locations using forecast.io package
    train_weather_info = fetch_weather_info(
            train_input_info,
            datetime.datetime(2017, 1, 1),
            '640590331b2eb20aca635216fcf6859f'
            )

    # Converting the extracted weather details into a Dataframe for later use
    train_weather_df = pd.DataFrame(train_weather_info)

    # Writing the intermediate Weather Dataframe into a CSV file for reference
    train_weather_df.to_csv('data/train_weather_data.csv', index=False)

    # Generating various models for predicting weather data
    train_temperature, train_pressure, train_humidity, train_conditions = (
            train_model(train_weather_df)
            )

    # List of locations to test the model
    input_test_list = None
    with open('data/test_file.txt') as input:
        input_test_list = [line.strip() for line in input]

    # Fetching location co-ordinates for the list of input Test locations
    test_input_info = fetch_location_info(input_test_list, err_file)

    # Start Date for predicting the Test Data
    start_date = datetime.datetime(2017, 6, 1)

    # Predicting weather data by using trained machine learning models
    test_weather_info = predict_weather_info(
        test_input_info,
        train_temperature,
        train_pressure,
        train_humidity,
        train_conditions,
        start_date
        )

    # Generating output dataframe so that we can write it in the file
    test_weather_df = pd.DataFrame(test_weather_info)

    # Choose the list of columns to be present in the output file
    output_cols = (
            ["Location",
             "Position",
             "Local Time",
             "Conditions",
             "Temperature",
             "Pressure",
             "Humidity"]
            )

    # Create pipe-separated output file along with header
    test_weather_df[output_cols].to_csv(
        "data/output_weather_info.psv",
        header=True,
        index=False,
        sep='|'
    )

    err_file.close()
