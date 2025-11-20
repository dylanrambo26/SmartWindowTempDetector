import network
import socket
import time
import json
import os
import _thread

CONFIG_FILE = "config.json"
_lock = _thread.allocate_lock()

def load_config():
    with _lock:
        if CONFIG_FILE in os.listdir():
            with open(CONFIG_FILE) as f:
                return json.load(f)
        else:
            default = {"open_temp": 65, "close_temp": 78}
            with open(CONFIG_FILE, "w") as f:
                json.dump(default, f)
            return default

def save_config(config):
    with _lock:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

def start_server():
    config = load_config()

    SSID = "SSID"
    PASSWORD = "PASSWORD"

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
    print("Listening on", addr)

    while True:
        conn, addr = s.accept()
        print("Connection from", addr)
        request = conn.recv(1024).decode()

        if "POST" in request:
            try:
                body = request.split("\r\n\r\n")[1]
                parts = body.split("&")
                for p in parts:
                    k, v = p.split("=")
                    if k == "open":
                        config["open_temp"] = int(v)
                    elif k == "close":
                        config["close_temp"] = int(v)
                save_config(config)
                print("✅ Updated config and saved to file:", config)
            except Exception as e:
                print("Error parsing form:", e)

        response = f"""
        <html><body>
            <h2>Temperature Control</h2>
            <form action="/" method="POST">
                Open below: <input type="number" name="open" value="{config['open_temp']}"><br>
                Close above: <input type="number" name="close" value="{config['close_temp']}"><br>
                <input type="submit" value="Save">
            </form>
        </body></html>
        """

        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        conn.sendall(response)
        conn.close()

if __name__ == "__main__":
    start_server()
