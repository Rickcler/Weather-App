#Reqeusts for Requesting the data
import requests
#PySimpleGUI for building the GUI
import PySimpleGUI as sg
#Coutntrynames to convert the Country Name to Iso-Code
import countrynames
#Base64 for converting the Icon from binary into ASCII
import base64

#Api Key from Openweathermap
api_key = "64cdfea0dbfd192437a08fdf01385a82"

#Function for changing whole country-name into ISO-Code
def get_country_code(country_name):
    try:
        country_code = countrynames.to_code(country_name)
        return country_code
    except AttributeError:
        return None
# Defining the layout of the initial input value
layout1 = [
    [sg.Text("Please enter your location data!")],
    [sg.Frame(
                layout =[
                [sg.Text('Country:', size = (20, 1)), sg.InputText(key="country", size = (20, 1))],
                [sg.Text('City:', size = (20, 1)), sg.InputText(key="city", size = (20, 1))]],
                title = "Enter here:", relief = sg.RELIEF_GROOVE
             )
    ],
    [sg.Button('Ok', button_color = ("black", "green"), bind_return_key = True), sg.Button('Cancel',button_color= ("white", "red"))]

]
# Creating the window
window1 = sg.Window('Weather App', layout1)

# Creating Event Loop to read in the Country/City data
while True:
    event, values = window1.read()
    #Ending Programm in it's closed or the cancel button is pressed
    if event in (None, 'Cancel'):
        window1.close()
        break
    #Creating Country and City variable from the Input, when Ok button is pressed
    elif event == 'Ok':
        Country = values["country"]
        City = values["city"]
        window1.close()
        break

#Next step is to get the ISO-Code from the Country input   
while True:
    if event in (None, "Cancel"):
        break
    try:
        #If it works the loop will not continue
        Country_Code = get_country_code(Country).lower()
        break
    except Exception as e:
        #If it doesn't work, the user gets another try until the Country can be converted into an ISO-Code
        while True:
            #Creating a new Layout that calls attention to the problem with the country name 
            layout2 =[
                    [sg.Text("That didn't work!")],
                    [sg.Text("You didn't put in the country name correctly. Please try again.")],
                    [sg.Frame(
                              layout =[
                                       [sg.Text('Country:', size = (20, 1)), sg.InputText(key="country", size = (20, 1))],
                                       [sg.Text('City:', size = (20, 1)), sg.InputText(key="city", size = (20, 1))]],
                                       title = "Enter here:", relief = sg.RELIEF_GROOVE
                             )
                    ],
                    [sg.Button('Ok', button_color = ("black", "green"), bind_return_key = True), sg.Button('Cancel',button_color= ("white", "red"))]
                    ]
            window2 = sg.Window('Weather App', layout2)
            event, values = window2.read()
            #Giving the user another option to close the window
            if event in (None, 'Cancel'):
                window2.close()
                break
            #Updating country and city names
            elif event == 'Ok':
                Country = values["country"]
                City = values["city"]
                window2.close()
                break
    #Leaving the loop in case the user Canceled or closed the window
    if event in (None, 'Cancel'):
        window2.close()
        break

#Creating a variable that combinesthe Cities Name and the Country Code in the way appropriate for the API 
city_name = f"{City},{Country_Code}"
#Creating URL Variable and requesting the data
url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
response = requests.get(url)

#Now checking if Openweather map accepted the request
while True:
    if response.status_code == 200: #Status_code 200 means that the request was succesfull
        break
    else:
        #As we made sure earlier, that the country name is right, it must about the city.
        while True:
            layout2 =[
                      [sg.Text("That didn't work!")],
                      [sg.Text("You didn't put the city name correctly. Please try again")]
                      [sg.Frame(
                                layout =[
                                        [sg.Text('Country:', size = (20, 1)), sg.InputText(key="country", size = (20, 1))],
                                        [sg.Text('City:', size = (20, 1)), sg.InputText(key="city", size = (20, 1))]],
                                        title = "Enter here:", relief = sg.RELIEF_GROOVE
                                )
                      ],
                      [sg.Button('Ok', button_color = ("black", "green"), bind_return_key = True), sg.Button('Cancel', button_color= ("white", "red"))]
                     ]
            window2 = sg.Window('Weather App', layout2)
            event, values = window2.read()
            #Closing the window if the user wants to
            if event in (None, 'Cancel'):
                window2.close()
                break
            #Updating the city variable
            elif event == 'Ok':
                City = values["city"]
                window2.close()
                break
    #Closing the window if the user wants to
    if event in (None, 'Cancel'):
        window2.close()
        break
    #Updating the request
    city_name = f"{City},{Country_Code}"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    

#Extracting the weather data from the JSON response
weather_data = response.json()
#Description of Weather
General_description =  weather_data['weather'][0]['description'].capitalize()
#Corresponding Icon
icon_id = weather_data["weather"][0]["icon"]
icon_url = f"http://openweathermap.org/img/wn/{icon_id}.png"
icon_response = requests.get(icon_url)
icon_base64 = base64.b64encode(icon_response.content)

#Temperature
Temperature_Celsius = weather_data["main"]["temp"]
Felt_Temperature = weather_data["main"]["feels_like"]   
#Wind Speed is in m/s
Wind_Speed = weather_data["wind"]["speed"]
#Humidity
Humidity = weather_data["main"]["humidity"]



layout3 = [[sg.Text(f"Weather in {City}:")],
           [sg.Frame( layout = [
                      [sg.Text(f"General Description: {General_description}"), sg.Image(data=icon_base64, size=(25, 25))],
                      [sg.Text(f"Temperature: {Temperature_Celsius}°C (Feels like {Felt_Temperature}°C)"), sg.Button("Fahrenheit")],
                      [sg.Text(f"Wind Speed: {Wind_Speed} m/s")],
                      [sg.Text(f"Humidity: {Humidity}%")]
                               ], title = "Results", relief = sg.RELIEF_GROOVE
                    )
                      
           ],
           [sg.Button("Close")]
          ]
window3 = sg.Window(title = "Results", layout = layout3)


#Showing the results and adding a button to change between Celsius and Fahrenheit
while True:
    event = window3.read()[0]
    if event in (None, "Close"):
        window3.close()
        break
    elif event == "Fahrenheit":
        Temperature_Fahrenheit = Temperature_Celsius * 9/5 + 32
        Felt_Temperature_Fahrenheit = Felt_Temperature * 9/5 +32
        layout3 = [[sg.Text(f"Weather in {City}:")],
                   [sg.Frame( layout = [
                                        [sg.Text(f"General Description: {General_description}"), sg.Image(data=icon_base64, size=(25, 25))],
                                        [sg.Text(f"Temperature: {Temperature_Fahrenheit}°F (Feels like {Felt_Temperature_Fahrenheit}°F)"), sg.Button("Celsius")],
                                        [sg.Text(f"Wind Speed: {Wind_Speed} m/s")],
                                        [sg.Text(f"Humidity: {Humidity}%")]
                                        ], title = "Results", relief = sg.RELIEF_GROOVE
                            )
                   ],
                   [sg.Button("Close")]
                  ]
        window3.close()
        window3 = sg.Window(title = "Results", layout = layout3)
    elif event == "Celsius":
        layout3 = [[sg.Text(f"Weather in {City}:")],
                   [sg.Frame( layout = [
                                        [sg.Text(f"General Description: {General_description}"), sg.Image(data=icon_base64, size=(25, 25))],
                                        [sg.Text(f"Temperature: {Temperature_Celsius}°C (Feels like {Felt_Temperature}°C)"), sg.Button("Fahrenheit")],
                                        [sg.Text(f"Wind Speed: {Wind_Speed} m/s")],
                                        [sg.Text(f"Humidity: {Humidity}%")]
                                        ], title = "Results", relief = sg.RELIEF_GROOVE
                            )
                   ],
                   [sg.Button("Close")]
                  ]
        window3.close()
        window3 = sg.Window(title = "Results", layout = layout3)