# boot.py - - runs on boot-up

import ubinascii

from machine import Pin, SPI
import max7219, utime

import network
import machine

# ap kampus
ssid = "Smart Parking"
password = "5m4rT_P4rk!Ng"

gmt7 = 3600 * 7

# local
mqtt_server = "192.168.0.100"
# mqtt_server = "raspberrypi.local"
mqtt_port = 1883
# public
# mqtt_server = "parking.sinaungoding.com"
# mqtt_port = 8095
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = "parkir/rekap"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))
d = max7219.Max7219(32, 8, spi, Pin(5), False)
d.brightness(5)
d.text("^_^", 0, 0)
d.show()
utime.sleep(3)

if not wlan.isconnected():
    print("connecting to network...")
    d.marquee("Connecting to "+ssid)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
print('Connection successful')
d.marquee("Connected with ip "+wlan.ifconfig()[0])
print(wlan.ifconfig())