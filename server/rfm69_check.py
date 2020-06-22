import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x

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
rfm = None
rfm_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'
prev_packet = None

while True:
        display.fill(0)

        try:
            rfm = adafruit_rfm9x.RFM9x(spi, CS, RESET, 916.0)
            rfm.encryption_key = rfm_key
            rfm.tx_power = 23
            display.text('RFM9x: Detected', 0, 0, 1)
            time.sleep(0.1)
        except RuntimeError as error:
            display.text('RFM9x: ERROR', 0, 0, 1)
            print('RFM9x Error: ', error)
            break

        if not btnA.value:
            # Send Button A
            display.fill(0)
            button_a_data = bytes("Button A!\r\n","utf-8")
            rfm.send(button_a_data)
            display.text('Sent Button A!', 25, 15, 1)
        elif not btnB.value:
            # Send Button B
            display.fill(0)
            button_b_data = bytes("Button B!\r\n","utf-8")
            rfm.send(button_b_data)
            display.text('Sent Button B!', 25, 15, 1)
        elif not btnC.value:
            # Send Button C
            display.fill(0)
            button_c_data = bytes("Button C!\r\n","utf-8")
            rfm.send(button_c_data)
            display.text('Sent Button C!', 25, 15, 1)
        
        display.show()
        time.sleep(0.1)
