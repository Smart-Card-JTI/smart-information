"""
Modul display information
Digunakan untuk menampilkan ketersediaan kantong parkir
"""

from machine import Pin, SPI
import max7219, utime

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))
d = max7219.Max7219(32, 8, spi, Pin(5), False)
d.brightness(5)
d.text("^_^",0,0)
d.show()
utime.sleep(3)

while True:
    d.marquee("Politeknik Negeri Malang...")
    d.marquee("Jos...")
