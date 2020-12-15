"""
Modul display information
Digunakan untuk menampilkan ketersediaan kantong parkir
"""

from time import *
import boot
import binascii
import ntptime
from umqttsimple import MQTTClient
import ujson
import machine

info = ""


class Kantong(object):
    def __init__(self, id, tanggal, kode, nama, terisi, sisa, catat, *args,
                 **kwargs):
        self.id = id
        self.tanggal = tanggal
        self.kode = kode
        self.nama = nama
        self.terisi = terisi
        self.sisa = sisa
        self.catat = catat


def sub_cb(topic, msg):
    try:
        print((topic, msg))
        print(msg.decode("utf-8"))
        parsed = ujson.loads(msg.decode("utf-8"))
        print("Length {} data {}".format(len(parsed), parsed))
        global info
        temp_info = ""
        for data in parsed:
            k = Kantong(**data)
            print("object kantong {} kode {}".format(k, k.kode))
            message = "{} terisi {} sisa {}".format(k.nama, k.terisi, k.sisa)
            temp_info = temp_info + message
        info = temp_info
        print("info {}".format(info))
    except OSError as e:
        restart_and_reconnect()


# MQTT
def connect_and_subscribe():
    print('Connecting to %s MQTT broker port %s, subscribed to %s topic' %
          (boot.mqtt_server, boot.mqtt_port, boot.topic_sub))
    boot.d.marquee(
        "Connecting to %s MQTT broker port %s, subscribed to %s topic" %
        (boot.mqtt_server, boot.mqtt_port, boot.topic_sub))
    client = MQTTClient(boot.client_id, boot.mqtt_server, port=boot.mqtt_port)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(boot.topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (boot.mqtt_server, boot.topic_sub))
    boot.d.marquee("Connected")
    sleep_ms(3000)
    return client


def restart_and_reconnect():
    boot.d.marquee("Error Connect " + boot.mqtt_server)
    sleep_ms(3000)
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    machine.reset()


# MQTT
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

# INIT TIME
ntptime.settime()


def day_name(arg):
    return {
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu"
    }.get(arg, None)


def __time2str(dt_time: tuple):
    return "{}, {:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        day_name(dt_time[6]), dt_time[0], dt_time[1], dt_time[2], dt_time[3],
        dt_time[4], dt_time[5])


while True:
    try:
        tm = time()
        NOW = localtime(tm + boot.gmt7)

        client.check_msg()

        boot.d.marquee("Smart Parking")
        boot.d.marquee("Politeknik Negeri Malang")
        boot.d.marquee(__time2str(NOW))
        if info is not None:
            boot.d.marquee(info)
        sleep(0.1)
    except OSError as e:
        restart_and_reconnect()