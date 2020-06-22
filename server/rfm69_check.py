import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69

btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

i2c = busio.I2C(board.SCL, board.SDA)

reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
display.fill(0)
display.show()
width = display.width
height = display.height

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm69 = None
prev_packet = None
rfm69.encryption_key=
b'#x01#x02#x03#x04#x05#x06#x07#x08#x01#x02#x03#x04#x05#x06#x07#x08'

while True:
        display.fill(0)

        try:
            rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 916.0)
            display.text('RFM69: Detected', 0, 0, 1)
            time.sleep(0.1)
        except RuntimeError as error:
            display.text('RFM69: ERROR', 0, 0, 1)
            print('RFM69 Error: ', error)
            break;

        if not btnA.value:
            display.text('Ada', width-85, height-7, 1)
            display.show()
            time.sleep(0.1)
        if not btnB.value:
            display.text('Fruit', width-75, height-7, 1)
            display.show()
            time.sleep(0.1)
        if not btnC.value:
            display.text('Radio', width-65, height-7, 1)
            display.show()
            time.sleep(0.1)

        display.show()
        time.sleep(0.1)
