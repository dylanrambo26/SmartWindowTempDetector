import network
import rp2
import sys
from time import sleep
from picozero import pico_led


def connect(ssid, password):
    print(f"connecting with {ssid} {password}")
    #connects to wlan
    wlan_sta = network.WLAN(network.STA_IF)
    
    #activate interfaces
    wlan_sta.active(True)
    
    #connect to network
    wlan_sta.connect(ssid,password)
    
    while wlan_sta.isconnected() == False:
        #pressing bootsel button quits program
        if rp2.bootsel_button() == 1:
            sys.exit()
        print("Waiting on Connection...")
        #led blinks whilst connection is being attempted
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
        
    ##long blink once connection is established
    if wlan_sta.isconnected() == True:
        pico_led.on()
        sleep(1.5)
        pico_led.off()
    #raspberry pi pico ip
    #ip = wlan_sta.ifconfig()[0]
    ip_sta = wlan_sta.ifconfig()[0]
    print(f'RPi connected on {ip_sta}')
    
    return ip_sta

if __name__ == "__main__":
    connect("Ribs&Rox.2", "S!lver84")

