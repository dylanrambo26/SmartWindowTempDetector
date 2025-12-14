# SmartWindowTempDetector
---

## Purpose
This project is an IOT sensor which would send a user a notification when their temperature outside a window would get below or above a certain threshold reminding them when to open/close their window. This would help people remember when to turn on/off their air conditioning during the summer in order to save energy.

## Hardware
- Breadboard
- Raspberry Pi Pico W
- DS18B20 Thermistor
- 9V Battery with 3.3V limiter

## Code Structure
- Experimental: This holds the experimental webserver for future plans to incorporate a webserver where the user could submit custom threshold values to their liking.
- Functional: The current working code that the project currently uses.
- Testing: Initial attempts at API testing

## TextBelt API
This project uses the open source TextBelt API https://textbelt.com/, with an API key a developer can cheaply send texts to their desired phone number in many different regions.
