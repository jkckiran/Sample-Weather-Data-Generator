# import necessary packages required for processing
import datetime
import numpy as np


'''
This will predict necessary variables based on respective trained models.
It iterates every 30 days from the Start Date for 180 days
Input - Testing Location Data along with ML models to predict the results.
Output - A dictionary with the required variables predicted by the models.
'''


def predict_weather_info(test_input_info, train_temperature, train_pressure,
                         train_humidity, train_conditions, start_date):

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

            # "Location" variable is from already fetched data
            weather_data['Location'] = (
                    weather_data.get('Location', [])
                    + [loc]
                    )

            # "Position" = Comma separated combination of lat, long and elev.
            geo_coords = str(lat) + ',' + str(lng) + ',' + str(elev)

            weather_data['Position'] = (
                    weather_data.get('Position', [])
                    + [geo_coords]
                    )

            # "Local Time" variable is of ISO8601 datetime format
            weather_data['Local Time'] = (
                    weather_data.get('Local Time', [])
                    + [new_date.isoformat()]
                    )

            # "Conditions" variable is predicted using the ML model
            cond = (
                    train_conditions.predict(
                            np.array([lat, lng, elev])
                            .reshape(1, -1))[0]
                    .lower()
                    )

            if 'clear' not in cond:
                cond = 'Rain'
            elif 'snow' in cond:
                cond = 'Snow'
            else:
                cond = 'Sunny'

            weather_data['Conditions'] = (
                    weather_data.get('Conditions', [])
                    + [cond]
                    )

            # "Temperature" variable is predicted using the ML model
            temp = (
                    train_temperature.predict(
                            np.array([lat, lng, elev])
                            .reshape(1, -1))[0][0]
                    )

            # The default Fahrenheit value is then converted into Celsius.
            temp_celsius = float("{0:.2f}".format((5.0 / 9.0) * (temp - 32)))

            weather_data['Temperature'] = (
                    weather_data.get('Temperature', [])
                    + [temp_celsius]
                    )

            # "Pressure" variable is predicted using the ML model
            pres = (
                    train_pressure.predict(
                            np.array([lat, lng, elev])
                            .reshape(1, -1))[0][0]
                    )

            pres = float("{0:.2f}".format(pres))

            weather_data['Pressure'] = (
                    weather_data.get('Pressure', [])
                    + [pres]
                    )

            # "Humidity" variable is predicted using the ML model
            hum = (
                    train_humidity.predict(
                            np.array([lat, lng, elev])
                            .reshape(1, -1))[0]
                    )

            weather_data['Humidity'] = (
                    weather_data.get('Humidity', [])
                    + [int(hum * 100)]
                    )

    return weather_data
