import network
import socket
import ure
from machine import Pin
import time
from picozero import pico_led

#AP creds
AP_SSID = 'PicoW_Config'
AP_PASSWORD = 'Password'

###HTML Pages
HTML_FORM = """<!doctype html><html><body>
<h1>WiFi Setup</h1>
<form method="POST" action="/save">
SSID: <input name="ssid" required><br>
Password: <input name="password" type="password"><br>
<input type="submit" value="Connect">
</form></body></html>"""

HTML_SUCCESS = "<html><body><h1>Credentials Recieved</h1></body></html>"

##global variables to store network creds
wifi_ssid = None
wifi_password = None


##boot the access point
def start_ap_mode():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(ssid = AP_SSID, key = AP_PASSWORD)
    print(f"AP mode has started. Connect to {AP_SSID} with password {AP_PASSWORD}")
    print(f"AP IP: {ap.ifconfig()[0]}")
    return ap

#main server
def run_server():
    
    global wifi_ssid
    global wifi_password
    
    pico_led.on()
    
    ap = start_ap_mode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 80))
    sock.listen(5)
    print("AP configuration for SSID and Password.")
    
    try:
        print("Waiting for browser POST...")
        while True:  # keep server alive until successful POST
            conn, ap_addr = sock.accept()
            print("Connection Established")
            request = b""
            # read full request
            while True:
                chunk = conn.recv(512)
                
                if not chunk:
                    break
                
                request += chunk
                
                if b"\r\n\r\n" in request:  # headers end
                    # check Content-Length
                    headers, _, body = request.partition(b"\r\n\r\n")
                    m = ure.search(b"Content-Length:\\s*(\\d+)", headers)
                    if m:
                        length = int(m.group(1))
                        while len(body) < length:
                            body += conn.recv(length - len(body))
                    break

            request_str = request.decode()
            
            if "GET /" in request_str:
                response = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + HTML_FORM
                conn.send(response.encode())
                conn.close()
                
            elif "POST /save" in request_str:
                # parse POST body
                headers, _, body = request.partition(b"\r\n\r\n")
                parts = dict([p.split('=',1) for p in body.decode().split('&') if '=' in p])
                wifi_ssid = parts.get('ssid','').replace('+',' ')
                wifi_password = parts.get('password','').replace('+',' ')
                
                
                success_response = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + HTML_SUCCESS
                conn.send(success_response.encode)
                conn.close()
                break  # exit the loop after POST
            
            else:
                conn.send("HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n404")
                conn.close()
                break
                
                
    except Exception as e:
        print("err", e)
    finally:
        try: sock.close()
        except: pass
        try: ap.active(False)
        except: pass
        pico_led.off()
        print("AP stopped")

#run_server()
