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
        
        if temp_f < 55 or 90 < temp_f:
            if (90 < temp_f and high == False):
                high = True
                textBeltAPI.close_window(90)
                print('Temp threshold exceeded!', temp_f)
            elif (temp_f < 55 and low == False):
                low = True
                textBeltAPI.open_window(55)
                print('Temp threshold exceeded!', temp_f)
        else:
            high = False
            low = False
            print('Temp', temp_f)
        
    

def main():
    ssid = 'SSID'
    password = 'PASSWORD'
    
    my_network.connect(ssid, password)
    
    run_thermo()
    
    
if __name__ == '__main__':
    main()





