import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69

from flask import current_app as app
from .models import Point
from . import db

class RadioBonnet(object):

    def __init(self):
        # Button A
        btnA = DigitalInOut(board.D5)
        btnA.direction = Direction.INPUT
        btnA.pull = Pull.UP

        # Button B
        btnB = DigitalInOut(board.D6)
        btnB.direction = Direction.INPUT
        btnB.pull = Pull.UP

        # Button C
        btnC = DigitalInOut(board.D12)
        btnC.direction = Direction.INPUT
        btnC.pull = Pull.UP

        # Create the I2C interface.
        i2c = busio.I2C(board.SCL, board.SDA)

        # 128x32 OLED Display
        reset_pin = DigitalInOut(board.D4)
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
        # Clear the display.
        display.fill(0)
        display.show()
        width = display.width
        height = display.height

        # Configure Packet Radio
        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
        prev_packet = None
        # Optionally set an encryption key (16 byte AES key). MUST match both
        # on the transmitter and receiver (or be set to None to disable/the default).
        rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

    def listen(self):
        while True:
            packet = None

            # check for packet rx
            packet = rfm69.receive()
            if packet is None:
                display.show()
                display.text('- Waiting for PKT -', 15, 20, 1)
            else:
                # Display the packet text and rssi
                display.fill(0)
                prev_packet = packet
                packet_text = str(prev_packet, "utf-8")
                display.text('RX: ', 0, 0, 1)
                display.text(packet_text, 25, 0, 1)
                valid = self.processPacket(packet_text)

                time.sleep(0.01)

    def processPacket(self,packetstr):
        valid = True
        value = float(packetstr)
        print(value)

        point = Point(data=value)
        db.session.add(point)
        db.session.comit()

        return valid,value
