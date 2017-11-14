# import necessary packages required for processing
import datetime
import forecastio


'''
This function generates weather related details for a particular location
It iterates every 7 days from the Start Date for 180 days
Input - locations with co-ordinates, start_date and the forecast.io api_key
Output - Dictionary file containing weather details for a particular location
'''


def fetch_weather_info(train_input_info, start_date, api_key):
    weather_info = {}

    for temp_info in train_input_info:
        for date_offset in range(0, 180, 7):

            forecast = forecastio.load_forecast(
                api_key,
                temp_info['Latitude'],
                temp_info['Longitude'],
                time=start_date + datetime.timedelta(date_offset),
                units="us"
            )

            # Temperature is not available in daily().data.
            # So fetch hourly().data to extract temperature values
            for hour in forecast.hourly().data:

                weather_info['Location'] = (
                 weather_info.get('Location', [])
                 + [temp_info['Location']]
                 )

                weather_info['Latitude'] = (
                 weather_info.get('Latitude', [])
                 + [temp_info['Latitude']]
                 )

                weather_info['Longitude'] = (
                 weather_info.get('Longitude', [])
                 + [temp_info['Longitude']]
                 )

                weather_info['Elevation'] = (
                 weather_info.get('Elevation', [])
                 + [temp_info['Elevation']]
                 )

                weather_info['Conditions'] = (
                 weather_info.get('Conditions', [])
                 + [hour.d.get('summary', '')]
                 )

                weather_info['Temperature'] = (
                 weather_info.get('Temperature', [])
                 + [hour.d.get('temperature', 75)]
                 )

                weather_info['Humidity'] = (
                 weather_info.get('Humidity', [])
                 + [hour.d.get('humidity', 0.5)]
                 )

                weather_info['Pressure'] = (
                 weather_info.get('Pressure', [])
                 + [hour.d.get('pressure', 1000)]
                 )

                weather_info['Time'] = (
                 weather_info.get('Time', [])
                 + [hour.d['time']]
                 )

    return weather_info
