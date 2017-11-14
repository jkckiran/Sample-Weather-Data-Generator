# Importing Supervised Learning Estimators.
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB


'''
This function takes the dataframe with location and weather details as input
It trains respective models based on input train data
And create models to predict temperature, pressure, humidity and conditions
The Independent Variable 'x' is the combination of lat, long and elev
The Dependent Variable 'y' differs for each model
'''


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
