import network
import time

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Režim Station
    wlan.active(True)
    if not wlan.isconnected():
        print("Připojuji se k WiFi:", ssid)
        wlan.connect(ssid, password)
        # Čekej, dokud není připojeno
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Úspěšně připojeno. IP adresa:", wlan.ifconfig()[0])
    return wlan

def get_html(led_state):
    try:
        with open("index.html", "r") as f:
            html = f.read()
        return html.replace("{{led_state}}", led_state)
    except Exception as e:
        return f"<html><body><h1>Chyba při načítání HTML: {e}</h1></body></html>"
    
