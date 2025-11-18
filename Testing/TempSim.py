import textBeltAPI as textBeltAPI
import time

class TemperatureSimulation:
    def __init__(self):
        self.lowTriggeredOnce = True
        self.highTriggeredOnce = False
    
    def tempSimulation(self, lowTemp, highTemp, simTime, step_time=1):
        """
        Simulates a temperature that goes from lowTemp to highTemp and back down
        over simTime seconds total.
    
        Parameters:
            lowTemp (float): starting and ending temperature
            highTemp (float): peak temperature
            simTime (int): total simulation time (seconds)
            step_time (float): time between steps (seconds)
        """
        # Number of steps for half the simulation (up or down)
        half_steps = int((simTime / 2) / step_time)
    
        # Generate the rising and falling temperature sequences
        rising = [lowTemp + i * (highTemp - lowTemp) / half_steps for i in range(half_steps)]
        falling = [highTemp - i * (highTemp - lowTemp) / half_steps for i in range(half_steps)]
        
        # Combine both parts
        temps = rising + falling
        
        highThreshold = 70
        lowThreshold = 65

        start_time = time.time()
        currentElapsedTime = 0
        for t in temps:
            currentElapsedTime = time.time() - start_time
            print(f"Temperature: {t:.2f} °F, Time: {currentElapsedTime:.2f} seconds")
            if not self.lowTriggeredOnce:
                self.low_temp_check(t, lowThreshold)
            elif not self.highTriggeredOnce:
                self.high_temp_check(t, highThreshold)
            time.sleep(step_time)
        
        total_elapsed = currentElapsedTime
        print(f"\nSimulation complete. Total elapsed time: {total_elapsed:.2f} seconds")

    def low_temp_check(self, temperature, lowTempThreshold):
        if(temperature < lowTempThreshold):
            textBeltAPI.open_window(lowTempThreshold)
            self.lowTriggeredOnce = True
            self.highTriggeredOnce = False

    def high_temp_check(self, temperature, highTempThreshold):
        if(temperature > highTempThreshold):
            textBeltAPI.close_window(highTempThreshold)
            self.highTriggeredOnce = True
            self.lowTriggeredOnce = False
        

def main():
    #Dummy data for testing API
    sim = TemperatureSimulation() 
    sim.tempSimulation(55,78,30,1)


if __name__ == "__main__":
    main()   