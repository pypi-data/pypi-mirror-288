import requests

"""
    Fetches the current weather for a given city.

    Parameters:
    - city (str): The name of the city.

    Returns:
    - dict: A dictionary containing temperature in Celsius, weather condition, and wind speed.
    - str: An error message if the city is not found.
"""
def GetWeather(city):

    city=city.lower()

    # If the city is not in the list, return an error message
    
    api_key = "4da0e8341db549c0b6c163519231608"

    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    response = requests.get(url)


    if response.status_code != 200:
        return "City not found"
    else:
        data = response.json()
        return {'temprature_c':data["current"]["temp_c"] , 'condition':data["current"]["condition"]["text"]}
    

"""
    Fetches the 5-day weather forecast for a given city.

    Parameters:
    - city (str): The name of the city.

    Returns:
    - list: A list of dictionaries, each containing the date, maximum temperature, minimum temperature, and weather condition.
    - str: An error message if the city is not found.
"""
def FutureForecast(city):
    city=city.lower()
    api_key = "4da0e8341db549c0b6c163519231608"

    url=f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=5&aqi=no&alerts=no"


    response = requests.get(url)    

    if response.status_code != 200:
        return "City not found"
    else:
        data=response.json()

        forecast = []

        for day in data["forecast"]["forecastday"]:
            forecast.append({
                "date": day["date"],
                "max_temp": day["day"]["maxtemp_c"],
                "min_temp": day["day"]["mintemp_c"],
                "condition": day["day"]["condition"]["text"]
            })

        return forecast


