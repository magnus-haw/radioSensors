import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69
import datetime

INTERVAL = 1.0
CACHE_INTERVAL = 3

class Experiment:
    def __init__(self, name):
        self.name = name

        i2c = busio.I2C(board.SCL, board.SDA)
        reset_pin = DigitalInOut(board.D4)
        self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
        self.display.fill(0)
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

        try:
            self.rfm = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
            self.rfm.encryption_key = rfm_key
            print('RFM69: Detected')
        except RuntimeError as error:
            print('RFM69 Error: ', error)

        self.sensors = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)
    
    def listen(self):
        while True:
            self.display.fill(0)

            packet = self.rfm.receive()
            if packet is None:
                yield None
                pass
            else:
                self.display.fill(0)
                self.prev_packet = packet
                packet_text = str(self.prev_packet, "utf-8")
                self.display.text('RX: ', 0, 0, 1)
                self.display.text(packet_text, 25, 0, 1)
                print('Received: ', packet_text)
                # self.cache.append({
                #     'data': float(packet_text)
                #     # 'timestamp': datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
                # })
                # cache_count+=1
                # if (cache_count >= CACHE_INTERVAL):
                #     yield self.cache
                #     self.cache.clear()
                #     cache_count = 0
                # else:
                #     yield None

            self.display.show()

            

class Sensor:
    def __init__(self, name):
        self.name = name
        self.cache = []