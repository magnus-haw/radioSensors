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
        self.stop = False
        # Optionally set an encryption key (16 byte AES key). MUST match both
        # on the transmitter and receiver (or be set to None to disable/the default).
        self.rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

    def listen(self):
        t0 = time.time()
        FLAG = False

        ### Radio packet loop 
        while not FLAG:          
            ### check for packet rx
            packet = None
            packet = self.rfm69.receive()
            if packet is None:
                self.display.text('- Waiting for PKT -', 15, 20, 1)
            else:
                ### Display the packet text 
                packet_text = str(packet, "utf-8")
                self.display.text('RX: ', 0, 0, 1)
                self.display.text(packet_text, 25, 0, 1)

                ### Parse data and add to database
                valid = self.processPacket(packet_text)
                    
            self.display.show()
            time.sleep(0.01)
            self.display.fill(0)
            
            # check FLAG conditions
            if not self.btnA.value or self.stop:
                # Check Button A
                FLAG = True
                self.display.text('- Done -', 15, 20, 1)
                self.display.show()
                time.sleep(0.005)

    def processPacket(self,packetstr):
        valid = True; sensor=None; value=None
        try:
            splitList = packetstr.strip().split(',')
            sensor_name,value = splitList[0], float(splitList[1])
            print(sensor_name,value)
        except:
            print("Packet processing error! Could not split")
            valid = False
            return valid,sensor,value
        
        exp = Experiment.query.get(self.experiment_id)
        sensor = Sensor.query.filter_by(name=sensor_name).first() 
        point = Point(data=value,sensor=sensor,experiment=exp)
        db.session.add(point)
        db.session.commit()
        #except:
        #    print("Sensor not present in database")
        #    valid = False
        return valid,sensor,value
