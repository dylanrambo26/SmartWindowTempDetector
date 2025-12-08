import socket
from time import sleep
from picozero import pico_temp_sensor
import machine
from machine import Pin
import sys
import onewire
import ds18x20

import my_network
import textBeltAPI

import _thread
import SmartWindowWebServer


def celsius_to_faren(temp_c):
    temp_f = temp_c *1.8
    temp_f += 32
    return temp_f

def run_thermo():
    #DS18B20 Setup
    #data line connected to digital pin 34, ow is now an object that can send data and power over a single data line
    #ds is a driver class for the wire object
    #roms gets the thermistors unique rom id
    one_wire = onewire.OneWire(Pin(28))
    ds = ds18x20.DS18X20(one_wire)
    roms = ds.scan()
    print('Found DS devices:', roms)
    
    high = False
    low = False
    
    #main loop to read temp and send
    while True:
        ds.convert_temp() #tell sensor to measure
        sleep(750/1000)
    
        #read and convert temp
        for rom in roms:
            temp_c = ds.read_temp(rom)
            temp_f = celsius_to_faren(temp_c)
        
        config = SmartWindowWebServer.load_config()
        print("Config:", config)

        #Set the open/close temp thresholds to the values specified by the user
        open_temp = config["open_temp"]
        close_temp = config["close_temp"]
        mode = config["mode"] # Winter or summer mode specified by user
        
        if mode == "summer":
            if (temp_f < open_temp or temp_f > close_temp):
                if (temp_f > close_temp and high == False):
                    high = True
                    textBeltAPI.close_window(close_temp, mode)
                    print('Temp threshold exceeded!', temp_f)
                elif (temp_f < open_temp and low == False):
                    low = True
                    textBeltAPI.open_window(open_temp, mode)
                    print('Temp threshold exceeded!', temp_f)
            else:
                high = False
                low = False
                print("Temp", temp_f)
        
        if mode == "winter":
            if (temp_f < close_temp or temp_f > open_temp):
                if (temp_f < close_temp and low == False):
                    low = True
                    textBeltAPI.close_window(close_temp, mode)
                    print('Temp threshold exceeded!', temp_f)
                elif (temp_f > open_temp and high == False):
                    high= True
                    textBeltAPI.open_window(open_temp, mode)
                    print('Temp threshold exceeded!', temp_f)
            else:
                high = False
                low = False
                print("Temp", temp_f)

def main():
    ssid = 'SSID'
    password = 'PASSWORD'
    
    my_network.connect(ssid, password)

    #Start the web server in another thread
    _thread.start_new_thread(SmartWindowWebServer.start_server, ())

    run_thermo()
    
    
if __name__ == '__main__':
    main()





