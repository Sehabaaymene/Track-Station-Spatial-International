import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 35.697071   # Your latitude
MY_LNG = -0.630799   # Your longitude
MY_EMAIL = "sehabaaymene1@gmail.com"
PASSWORD = "wyttvbdwnvxpjagh"


def is_iss_overhead():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    longitude = float(data_iss["iss_position"]["longitude"])
    latitude = float(data_iss["iss_position"]["latitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= longitude <= MY_LAT + 5 and MY_LNG - 5 <= latitude <= MY_LAT + 5:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    response_sun = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response_sun.raise_for_status()
    data_sun = response_sun.json()

    # Getting the sunrise and sunset time by hour using split method.
    sunrise = int(data_sun["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_sun["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP("smtp.gmail.com") as connection :
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="sehabaaymene1@gmail.com", msg="Subject ISS OVER HEAD\n\n"
                                                                                            "See ISS it's over you.")
