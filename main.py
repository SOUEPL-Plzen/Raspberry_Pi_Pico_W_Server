import socket
import machine
import wlan  # import vlastního modulu wlan.py

SSID = "Vodafone-1531"
PASSWORD = "7WWN5eUymt5usuke"

led = machine.Pin("LED", machine.Pin.OUT)

my_state = False
led_state = "OFF"

def main():
    global my_state, led_state  # DŮLEŽITÉ DOPSAT

    # Připojení k Wi-Fi
    mywlan = wlan.connect_to_wifi(SSID, PASSWORD)
    ip = mywlan.ifconfig()[0]

    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    
    print(f"Web server běží na http://{ip}:80/")

    while True:
        cl, addr = s.accept()
        print("Klient se připojil z IP:", addr)

        request = cl.recv(2048)
        if not request:
            cl.close()
            continue

        request_str = request.decode("utf-8")
        print("Požadavek:", request_str)

        lines = request_str.split("\r\n")
        request_line = lines[0].split()
        if len(request_line) < 2:
            cl.close()
            continue
        method = request_line[0]
        path = request_line[1]

        if method == "POST" and path == "/":
            if "action=on" in request_str:
                my_state = True
                led_state = "ON"
                led.value(1)
            elif "action=off" in request_str:
                my_state = False
                led_state = "OFF"
                led.value(0)

        response_body = wlan.get_html(led_state)
        response = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n\r\n"
            + response_body
        )
        cl.sendall(response)
        cl.close()
        
main()
