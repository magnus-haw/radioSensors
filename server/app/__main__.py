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
rfm = None
rfm_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'
prev_packet = None

while True:
        display.fill(0)

        # Check if RFM69 is reachable
        try:
            rfm = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
            rfm.encryption_key = rfm_key
            display.text('RFM69: Detected', 0, 0, 1)
            print('RFM69: Detected')
            time.sleep(0.1)
        except RuntimeError as error:
            display.text('RFM69: ERROR', 0, 0, 1)
            print('RFM69 Error: ', error)
            break

        # Receiving sensor data
        packet = rfm.receive()
        if packet is None:
            pass
        else:
            display.fill(0)
            prev_packet = packet
            packet_text = str(prev_packet, "utf-8")
            display.text('RX: ', 0, 0, 1)
            display.text(packet_text, 25, 0, 1)
            print("Received: ", packet_text)
            time.sleep(1)

        # Buttons
        if not btnA.value:
            # Send Button A
            display.fill(0)
            button_a_data = bytes("request_sensor","utf-8")
            rfm.send(button_a_data)
            display.text('Sent Button A!', 25, 15, 1)
            print("Sent A")
        elif not btnB.value:
            # Send Button B
            display.fill(0)
            button_b_data = bytes("listen_ready","utf-8")
            rfm.send(button_b_data)
            display.text('Sent Button B!', 25, 15, 1)
            print("Sent B")
        elif not btnC.value:
            # Send Button C
            display.fill(0)
            button_c_data = bytes("listen_stop","utf-8")
            rfm.send(button_c_data)
            display.text('Sent Button C!', 25, 15, 1)
            print("Sent C")
        
        display.show()
        time.sleep(0.1)