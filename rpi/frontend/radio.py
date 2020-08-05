import time
import busio
import json
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69
import datetime
import decimal

from . import db
from .models import Sensor, Point

INTERVAL = 1.0
CACHE_INTERVAL = 3
active_experiment = None

class RadioBonnet:
    def __init__(self):
        self.active = []
        self.disabled = []

        i2c = busio.I2C(board.SCL, board.SDA)
        reset_pin = DigitalInOut(board.D4)
        self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
        self.display.fill(0)
        self.display.show()

        self.display.text('test', 0, 0, 1)
        self.display.show()

        # Assign Button Pins
        self.button = {}

        self.button['A'] = DigitalInOut(board.D5)
        self.button['A'].direction = Direction.INPUT
        self.button['A'].pull = Pull.UP

        self.button['B'] = DigitalInOut(board.D6)
        self.button['B'].direction = Direction.INPUT
        self.button['B'].pull = Pull.UP

        self.button['C'] = DigitalInOut(board.D12)
        self.button['C'].direction = Direction.INPUT
        self.button['C'].pull = Pull.UP

        # Setup RFM
        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        rfm_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'
        self.prev_packet = None

        while True:
            try:
                self.rfm = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
                self.rfm.encryption_key = rfm_key
                self.display.fill(0)
                self.display.text('RFM69: Detected', 0, 0, 1)
                self.display.show()
                break
            except RuntimeError as error:
                self.display.fill(0)
                self.display.text('RFM69 Error: {}'.format(error), 0, 0, 1)
                self.display.show()
                time.sleep(INTERVAL)
    
    def disable(self, name):
        if name in self.active:
            self.active.pop(name)
            self.disabled.append(name)
            return name
        else: return None
    
    def enable(self, name):
        if name in self.disabled:
            self.disabled.pop(name)
            self.active.append(name)
            return name
        else: return None

    def get_experiment(self):
        global active_experiment
        return active_experiment

    def set_experiment(self, experiment):
        global active_experiment
        active_experiment = experiment

    def listen(self):
        global active_experiment
        while True:
            print(active_experiment)
            if active_experiment:
                packet = self.rfm.receive()
                if packet is None: pass
                else:
                    self.prev_packet = packet

                    try:
                        packet_data = str(self.prev_packet, 'utf-8')
                    except UnicodeDecodeError: pass

                    try:
                        json_data = json.loads(packet_data)
                        
                        self.display.fill(0)
                        self.display.text('Received:', 0, 0, 1)
                        self.display.text(json_data['name'], 0, 12, 1)
                        self.display.text('{} {}'.format(
                            json_data['value'],
                            json_data['unit']
                        ), 0, 24, 1)
                        self.display.show()

                        if json_data['name'] in self.disabled: pass
                        elif json_data['name'] not in self.active: self.disabled.append(json_data['name'])
                        else:
                            sensor = Sensor.query.filter_by(name=json_data['name']).first()
                            if not sensor:
                                sensor = Sensor(name=json_data['name'], unit=json_data['unit'])
                                db.session.add(sensor)
                            point = Point(
                                data=json_data['value'],
                                sensor=sensor,
                                experiment=active_experiment
                            )
                            db.session.add(point)
                            db.session.commit()
                            time.sleep(INTERVAL)
                    except json.decoder.JSONDecodeError: pass
        