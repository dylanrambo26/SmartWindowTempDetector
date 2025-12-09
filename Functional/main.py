from time import sleep, ticks_ms, ticks_diff
from machine import Pin
import onewire
import ds18x20
import _thread
import network

from picozero import pico_temp_sensor
import my_network
import ap_config
import textBeltAPI

LOW_THRESH = 68
HIGH_THRESH = 85

SSID = None
PASSWORD = None

WLAN_CHECK = 10  #check connection every 10 seconds

def url_decode(cred):
    cred = cred.replace('+', ' ')
    cred = cred.replace('%26', '&')    # &
    cred = cred.replace('%21', '!')    # !
    cred = cred.replace('%5F', '_')    # _
    cred = cred.replace('%28', '(')    # (
    cred = cred.replace('%29', ')')    # )
    return cred

def ensure_connection(sta_if, ssid, password, last_attempt):
    if sta_if.isconnected():
        return last_attempt
    else:
        my_network.connect(SSID, PASSWORD)
        return ticks_ms()
    
def run_thermo():
    #wlan object creation
    sta_if = network.WLAN(network.STA_IF) 
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
    
    last_wlan_check = 0
    
    #main loop to read temp and send
    while True:     
        #checks connection every 10 seconds, represented in miliseconds
        if ticks_diff(ticks_ms(), last_wlan_check) >= WLAN_CHECK * 1000:
            last_wlan_check_time = ticks_ms()
            last_wlan_check = ensure_connection(sta_if, SSID, PASSWORD, last_wlan_check)
        
        #sta_if.disconnect() - to test reconnection process
            
        
        ds.convert_temp() #tell sensor to measure
        sleep(750/1000)
    
        #read and convert temp
        for rom in roms:
            temp_c = ds.read_temp(rom)
            temp_f = celsius_to_faren(temp_c)
        
        if temp_f < LOW_THRESH or HIGH_THRESH < temp_f:
            if (HIGH_THRESH < temp_f and high == False):
                high = True
                textBeltAPI.close_window(HIGH_THRESH)
                print('Temp threshold exceeded!', temp_f)
            elif (temp_f < LOW_THRESH and low == False):
                low = True
                textBeltAPI.open_window(LOW_THRESH)
                print('Temp threshold exceeded!', temp_f)
        else:
            high = False
            low = False
            print('Temp', temp_f)
        

    
def celsius_to_faren(temp_c):
    temp_f = temp_c *1.8
    temp_f += 32
    return temp_f


def main ():

    #_thread.start_new_thread(smart_window_web_server.start_server, ())
    #smart_window_web_server.load_config()
    global SSID
    global PASSWORD
    
    if not SSID or not PASSWORD:
        print("Running AP to get Credentials")
        
        """
        _thread.start_new_thread(ap_config.run_server, ())
        
        #wait fro globals to update
        while ap_config.wifi_ssid is None and ap_config.wifi_password is None:
            print(f"Waiting for global Update")
            sleep(6)
            
        SSID = ap_config.wifi_ssid
        PASSWORD = ap_config.wifi_password
        """
        ap_config.run_server()  # blocking, waits for POST
        SSID = ap_config.wifi_ssid
        PASSWORD = ap_config.wifi_password
    
    SSID = url_decode(ap_config.wifi_ssid)
    PASSWORD = url_decode(ap_config.wifi_password)
    
    sleep(2)
    print(f"creds: {SSID} {PASSWORD}")
    
    #put thermo in the thread rather than the web server

    my_network.connect(SSID, PASSWORD)
    print('connected')
    
    ##run thermometer
    run_thermo()
    
if __name__ == "__main__":
    main()
    
    





