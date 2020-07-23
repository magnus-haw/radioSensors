import time
import busio
import json
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69
import datetime

INTERVAL = 1.0
CACHE_INTERVAL = 3

class RadioBonnet:
    def __init__(self):
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
    
    def listen(self):
        while True:
            packet = self.rfm.receive()
            if packet is None: pass
            else:
                self.prev_packet = packet

                try:
                    packet_data = str(self.prev_packet, 'utf-8')
                except UnicodeDecodeError: continue

                try:
                    json_data = json.loads(packet_data)
                    yield(json_data)
                    self.display.fill(0)
                    self.display.text('Received:', 0, 0, 1)
                    self.display.text(json_data['name'], 25, 0, 1)
                    self.display.text('{} {}'.format(
                        json_data['value'],
                        json_data['unit']
                    ), 0, 25, 1)
                    self.display.show()
                    time.sleep(INTERVAL)
                except json.decoder.JSONDecodeError: pass