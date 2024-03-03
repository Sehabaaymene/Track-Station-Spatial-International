import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 35.697071   # Your latitude
MY_LNG = -0.630799   # Your longitude
MY_EMAIL = "your_mail@gamil.com"
PASSWORD = "Your_Password"


# To check if ISS is overhead.
def is_iss_overhead():

    # API of the ISS.
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    # Live longitude and latitude of the ISS.
    longitude = float(data_iss["iss_position"]["longitude"])
    latitude = float(data_iss["iss_position"]["latitude"])

    # Check if your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= longitude <= MY_LAT + 5 and MY_LNG - 5 <= latitude <= MY_LAT + 5:
        return True


# Check if it's night, So you be able to see it clearly.
def is_night():

    # Parameters of your Current location.
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    # API of the Sun position according to your place.
    response_sun = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response_sun.raise_for_status()
    data_sun = response_sun.json()

    # Getting the sunrise and sunset time by hour using split method.
    sunrise = int(data_sun["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_sun["results"]["sunset"].split("T")[1].split(":")[0])

    # The current hour time.
    time_now = datetime.now().hour

    # Checking if it's night by returning True if it is.
    if time_now >= sunset or time_now <= sunrise:
        return True


# Checking every 60 sec.
while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="sehabaaymene1@gmail.com", msg="Subject ISS OVER HEAD\n\n"
                                                                                            "See ISS it's over you.")
