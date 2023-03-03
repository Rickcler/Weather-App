#Reqeusts for Requesting the data
import requests
# PySimpleGUI for building the GUI
import PySimpleGUI as sg
# PyCountry to convert the Country Name to Iso-Code
import pycountry

#Api Key from Openweathermap
api_key = "64cdfea0dbfd192437a08fdf01385a82"

#Function for changing whole country-name into ISO-Code
def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2
    except AttributeError:
        return None
# Defining the layout of the window
layout1 = [
    [sg.Text('Enter your country:'), sg.InputText(key="country")],
    [sg.Text('Enter your city:'), sg.InputText(key="city")],
    [sg.Button('Ok'), sg.Button('Cancel')]
]
# Creating the window
window1 = sg.Window('Weather App', layout1)

# Creating Event Loop to read in the Country/City data
while True:
    event, values = window1.read()
    if event in (None, 'Cancel'):
        window1.close()
        break
    elif event == 'Ok':
        Country = values["country"]
        City = values["city"]
        window1.close()
        break


while True:
    try:
        Country_Code = get_country_code(Country).lower()
        break
    except Exception as e:
        while True:
            layout2 =[
                    [sg.Text("That didn't work! Please try again.")],
                    [sg.Text("You didn't put in the country name correctly. Please use the official English name")],
                    [sg.Text('Enter your country:'), sg.InputText(key="country")],
                    [sg.Text('Enter your city:'), sg.InputText(key="city")],
                    [sg.Button('Ok'), sg.Button('Cancel')]
                    ]
            window2 = sg.Window('Weather App', layout2)
            event, values = window2.read()
            if event in (None, 'Cancel'):
                window2.close()
                break
            elif event == 'Ok':
                Country = values["country"]
                City = values["city"]
                window2.close()
                break
    if event in (None, 'Cancel'):
        window2.close()
        break


city_name = f"{City},{Country_Code}"
url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
response = requests.get(url)

while True:
    if response.status_code == 200:
        break
    else:
        while True:
            layout2 =[
                      [sg.Text("That didn't work! Please try again.")],
                      [sg.Text("Please enter the city in the countries language")],
                      [sg.Text('Enter your city:'), sg.InputText(key="city")],
                      [sg.Button('Ok'), sg.Button('Cancel')]
                     ]
            window2 = sg.Window('Weather App', layout2)
            event, values = window2.read()
            if event in (None, 'Cancel'):
                window2.close()
                break
            elif event == 'Ok':
                City = values["city"]
                window2.close()
                break
    if event in (None, 'Cancel'):
        window2.close()
        break
    city_name = f"{City},{Country_Code}"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    

#Extracting the weather data from the JSON response
weather_data = response.json()
#Description of Weather
General_description =  weather_data['weather'][0]['description']
#Temperature
Temperature_Celsius = weather_data["main"]["temp"]
Felt_Temperature = weather_data["main"]["feels_like"]   
#Wind Speed is in m/s
Wind_Speed = weather_data["wind"]["speed"]
#Humidity
Humidity = weather_data["main"]["humidity"]

layout3 = [ 
          [sg.Text(f"General Description: {General_description}")],
          [sg.Text(f"Temperature: {Temperature_Celsius}°C(Feels like {Felt_Temperature}°C)")],
          [sg.Text(f"Wind Speed: {Wind_Speed} m/s")],
          [sg.Text(f"Humidity: {Humidity}%")],
          [sg.Button("Close")]
]
window3 = sg.Window(title = "Results", layout = layout3)

while True:
    event = window3.read()[0]
    if event in (None, "Close"):
        window3.close()
        break
