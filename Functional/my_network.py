import network
import rp2
from time import sleep
from picozero import pico_led

def connect(ssid, password):
    #connects to wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        #pressing bootsel button quits program
        if rp2.bootsel_button() == 1:
            sys.exit()
        print('Waiting for connection...')
        #led blinks whilst connection is being attempted
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
        
    ##long blink once connection is established
    if wlan.isconnected() == True:
        pico_led.on()
        sleep(1.5)
        pico_led.off()
    #raspberry pi pico ip
    ip = wlan.ifconfig()[0]
    print(f'RPi connected on {ip}')
    return ip

