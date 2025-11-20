#main.py
import _thread
import time
import textBeltAPI

def main():
    print("Starting main logic...")
    textBeltAPI.open_window(70)

    

    while True:
        config = SmartWindow2.load_config()
        print("Current config:", config)

        open_temp = config["open_temp"]
        close_temp = config["close_temp"]



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
