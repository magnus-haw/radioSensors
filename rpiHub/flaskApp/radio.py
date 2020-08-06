"""
Example for using the RFM69HCW Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69

from flask import current_app as app
from .models import Sensor, Experiment, Calibration, Point
from . import db

class RadioBonnet(object):

    ### Initialize buttons, display, and radio
    def __init__(self):
        # Button A
        self.btnA = DigitalInOut(board.D5)
        self.btnA.direction = Direction.INPUT
        self.btnA.pull = Pull.UP

        # Button B
        self.btnB = DigitalInOut(board.D6)
        self.btnB.direction = Direction.INPUT
        self.btnB.pull = Pull.UP

        # Button C
        self.btnC = DigitalInOut(board.D12)
        self.btnC.direction = Direction.INPUT
        self.btnC.pull = Pull.UP
        
        # Create the I2C interface.
        i2c = busio.I2C(board.SCL, board.SDA)

        # 128x32 OLED Display
        reset_pin = DigitalInOut(board.D4)
        self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
        # Clear the display.
        self.display.fill(0)
        self.display.show()

        # Configure Packet Radio
        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
        # Optionally set an encryption key (16 byte AES key). MUST match both
        # on the transmitter and receiver (or be set to None to disable/the default).
        self.rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

    def listen(self,lock,exp_id):
        t0 = time.time()
        FLAG = False

        ### Radio packet loop 
        while not FLAG:          
            ### check for packet rx
            packet = None
            packet = rfm69.receive()
            if packet is None:
                display.text('- Waiting for PKT -', 15, 20, 1)
            else:
                ### Display the packet text 
                packet_text = str(packet, "utf-8")
                display.text('RX: ', 0, 0, 1)
                display.text(packet_text, 25, 0, 1)

                ### Parse data and add to database
                valid,sensor_id,value = self.processPacket(packet_text)
                if valid:
                    self.postData(exp_id,sensor_id,value)
                    
            display.show()
            time.sleep(0.005)
            display.fill(0)
            
            # check FLAG conditions
            if not btnA.value:
                # Check Button A
                FLAG = True
                display.text('- Done -', 15, 20, 1)
                display.show()
                time.sleep(0.005)

    def processPacket(self,packetstr):
        valid = True; sensor_id=None; value=None
        try:
            splitList = packetstr.strip().split(',')
            sensor_id,value = int(splitList[0]), float(splitList[1])
        except:
            print("Packet processing error! Could not split")
            valid = False
        return valid,sensor_id,value

    def postData(self,exp_id,sensor_id,value):
        point = Point(data=value,sensor=sensor_id,experiment=exp_id)
        db.session.add(point)
        db.session.commit()
