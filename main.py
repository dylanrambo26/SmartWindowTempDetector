import _thread
import time
import textBeltAPI
import SmartWindowWebServer

def main():

    #Start at default state
    lowTriggeredOnce = False 
    highTriggeredOnce = False

    while True:
        #currentTemp = TEMP_FROM_SENSOR_HERE

        #Load the config file from the smart window webserver
        config = SmartWindowWebServer.load_config()
        print("Current config:", config)

        #Set the open/close temp thresholds to the values specified by the user
        open_temp = config["open_temp"]
        close_temp = config["close_temp"]
        mode = config["mode"] # Winter or summer mode specified by user
        
        # Since mode is summer, the window should be closed when the temp is higher than the close temp and opened when lower than the open temp
        # lowTriggeredOnce and highTriggeredOnce ensure that only one text is sent per threshold pass
        if mode == "summer":
            if not lowTriggeredOnce:
                if currentTemp < open_temp:
                    textBeltAPI.open_window(open_temp,mode) #Call the textbelt API
                    lowTriggeredOnce = True
                    highTriggeredOnce = False
            if not highTriggeredOnce:
                if currentTemp > close_temp:
                    textBeltAPI.close_window(close_temp,mode) #Call the textbelt API
                    highTriggeredOnce = True
                    lowTriggeredOnce = False

         # Since mode is winter, the window should be closed when the temp is lower than the close temp and opened when higher than the open temp            
        if mode == "winter":
            if not highTriggeredOnce:
                if currentTemp > open_temp:
                    textBeltAPI.open_window(open_temp,mode) #Call the textbelt API
                    lowTriggeredOnce = False
                    highTriggeredOnce = True
            if not lowTriggeredOnce:
                if currentTemp < close_temp:
                    textBeltAPI.close_window(close_temp,mode) #Call the textbelt API
                    highTriggeredOnce = False
                    lowTriggeredOnce = True

        time.sleep(5) # Ensure that config and temperature are only checked every 5 seconds
    
#Start the web server in another thread
_thread.start_new_thread(SmartWindowWebServer.start_server, ())

#Run main logic
main()