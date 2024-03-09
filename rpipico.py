import socket
import network
from time import sleep
from machine import Pin
import dht


ssid = 'Mrsh77'
password = '1m77n2299215r77#'


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip,80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    #print(connection)
    return connection

led_pin = Pin(0,Pin.OUT)
led_pin.value(0)


dht_sensor = dht.DHT11(Pin(15))

def air_params():
    sleep(4)
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    return temp, humidity
    
try:
    air_params()
    ip = connect()
    connection = open_socket(ip)
    while True:
        # Accept a connection from a client
        client, addr = connection.accept()
        print(f'Connected to {addr}')
        while True:
            # Receive data from the client
            data = client.recv(1024)
            if data:
                # Print the data to the console
                print(data)
                if data == b'o':
                    led_pin.value(1)
                    
                elif data == b'f':
                    led_pin.value(0)
                    
                # Send a response back to the client
                elif data == b"temp":
                    raw_temp, _ = air_params()
                    print(raw_temp)
                    final_temp = str(raw_temp).encode()
                    client.send(final_temp)
                    
                elif data == b"humidity":
                    _, raw_hum = air_params()
                    print(raw_hum)
                    final_hum = str(raw_hum).encode()
                    client.send(final_hum)

except KeyboardInterrupt:
    # Close the server socket
    connection.close()
    machine.reset()
