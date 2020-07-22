import busio
from digitalio import DigitalInOut
import board
import adafruit_ssd1306
import adafruit_rfm69
import datetime

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
display.fill(0)
display.show()

# Setup RFM
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# rfm_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'
prev_packet = None

try:
    rfm = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
    # rfm.encryption_key = rfm_key
    print('RFM69: Detected')
except RuntimeError as error:
    print('RFM69 Error: ', error)

while True:
    display.fill(0)

    packet = rfm.receive()
    if packet is None:
        print("No packet recieved.")
        print(packet)
        pass
    else:
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('RX: ', 0, 0, 1)
        display.text(packet_text, 25, 0, 1)
        print('Received: ', packet_text)

    display.show()
