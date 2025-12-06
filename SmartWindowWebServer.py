import network
import socket
import time
import json
import os
import _thread

#JSON file for temps and mode from user
CONFIG_FILE = "config.json" 

#Mutex lock to prevent other threads from modifying config
_lock = _thread.allocate_lock()

# Load config with values
def load_config():
    with _lock:
        if CONFIG_FILE in os.listdir():
            with open(CONFIG_FILE) as f:
                config = json.load(f)

            # Ensure new fields exist even if old config file is missing them
            if "mode" not in config:
                config["mode"] = "summer"
            return config

        #Set default values for the config if not specified
        else:
            default = {"open_temp": 65, "close_temp": 78, "mode": "summer"}
            with open(CONFIG_FILE, "w") as f:
                json.dump(default, f)
            return default

# Write to the config file
def save_config(config):
    with _lock:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

# Smart Window web server, open webserver ui at the address specified by the output with pico connected to wifi
def start_server():
    config = load_config()

    SSID = "SSID"
    PASSWORD = "PASSWORD"
    
    # Connect to WiFi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(0.5)
    print("Connected! IP:", wlan.ifconfig()[0])

    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr) #Address to open in web browser

    # Wait for incoming connections from a browser
    while True:
        conn, addr = s.accept() # Accept connection from browser
        print("Connection from", addr)
        request = conn.recv(1024).decode()

        # Proccess user submitted form from browser
        if "POST" in request:
            try:
                body = request.split("\r\n\r\n")[1]
                parts = body.split("&")

                # Parse the config for the values
                for p in parts:
                    if "=" not in p:
                        continue
                    k, v = p.split("=")

                    if k == "open":
                        config["open_temp"] = int(v)
                    elif k == "close":
                        config["close_temp"] = int(v)
                    elif k == "mode":
                        config["mode"] = v  # "winter" or "summer"

                #Save updated config
                save_config(config)
                print("Updated config and saved to file: ", config)

            except Exception as e:
                print("Error parsing form:", e)

        mode_checked_winter = "checked" if config["mode"] == "winter" else ""
        mode_checked_summer = "checked" if config["mode"] == "summer" else ""

        #Webpage HTML
        response = f"""
        <html><body>
            <h2>Smart Window Temperature Control</h2>

            <form action="/" method="POST">

                <h3>Mode</h3>
                <label>
                    <input type="radio" name="mode" value="winter" {mode_checked_winter}>
                    Winter Mode (open below, close above)
                </label><br>

                <label>
                    <input type="radio" name="mode" value="summer" {mode_checked_summer}>
                    Summer Mode (open above, close below)
                </label><br><br>

                <h3>Temperature Settings</h3>
                Open threshold:
                <input type="number" name="open" value="{config['open_temp']}"><br>

                Close threshold:
                <input type="number" name="close" value="{config['close_temp']}"><br><br>

                <input type="submit" value="Save">
            </form>
        </body></html>
        """

        #Send response to browser
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        conn.sendall(response)
        conn.close()

if __name__ == "__main__":
    start_server()
