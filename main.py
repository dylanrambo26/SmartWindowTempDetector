#main.py
import _thread
import time
import textBeltAPI

def main():
    print("Starting main logic...")
    # textBeltAPI.open_window(70)

    #Start at default state
    lowTriggeredOnce = False 
    highTriggeredOnce = False

    while True:
        #currentTemp = TEMP_FROM_SENSOR_HERE

        config = SmartWindow2.load_config()
        print("Current config:", config)

        open_temp = config["open_temp"]
        close_temp = config["close_temp"]

        if not lowTriggeredOnce:
            if currentTemp < open_temp:
                textBeltAPI.open_window(open_temp)
                lowTriggeredOnce = True
                selfhighTriggeredOnce = False
        if not highTriggeredOnce:
            if currentTemp > close_temp:
                textBeltAPI.close_window(close_temp)
                highTriggeredOnce = True
                lowTriggeredOnce = False

        # Example placeholder logic
        # temp = temp_sensor.read_fahrenheit()
        # if temp < open_temp:
        #     open_window()
        # elif temp > close_temp:
        #     close_window()

        time.sleep(5)
    
#Start the web server in another thread
_thread.start_new_thread(SmartWindow2.start_server, ())

#Run main logic
main()
