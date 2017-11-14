# import necessary packages required for processing
import requests


'''
This function takes a list of locations as input.
Generates Location Details for training or testing the model.
Error file will be created for the locations whose data are not available
'''


def fetch_location_info(input_list, err_file):

    # URL which gives us Latitude, Longitude values
    LatLong_URL = (
     'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
     )

    # URL which gives us Elevation values
    Elevation_URL = (
     'https://maps.googleapis.com/maps/api/elevation/json?locations='
     )

    # Initializing Error Logs with relevant title for writing error records
    err_line_header = "Logging Location Data Errors"
    print(err_line_header, file=err_file)

    # Insert a new line in the error file after the Error Header
    print("\n", file=err_file)

    # Fetch and Extract Location details from google maps
    input_info = []

    for location in input_list:
        temp_info = {'Location': location}
        latlong_response = requests.get(LatLong_URL + location).json()

        if latlong_response.get('results'):
            for latlong_results in latlong_response.get('results'):
                latlong = (
                    latlong_results
                    .get('geometry', '0')
                    .get('location', '0')
                    )

                temp_info['Latitude'] = latlong.get('lat', '0')
                temp_info['Longitude'] = latlong.get('lng', '0')

                elevation_response = requests.get(
                    Elevation_URL
                    + str(temp_info['Latitude'])
                    + ','
                    + str(temp_info['Longitude'])
                    ).json()

                if elevation_response.get('results'):
                    for elevation_results in elevation_response.get('results'):
                        temp_info['Elevation'] = (
                            elevation_results.get('elevation', '0'))

                        input_info.append(temp_info)
                        break
                else:
                    print("Elevation_URL is not fetching values for {}"
                          .format(location),
                          file=err_file
                          )
                break
        else:
            print("LatLong_URL is not fetching values for {}"
                  .format(location),
                  file=err_file
                  )

    print("\n", file=err_file)
    return input_info
