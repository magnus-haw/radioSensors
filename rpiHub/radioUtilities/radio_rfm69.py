"""
Example for using the RFM69HCW Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import the RFM69 radio module.
import adafruit_rfm69




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

npackets=0
t0 = time.time()
FLAG = False
datastr = ""
while not FLAG:
    packet = None
    # draw a box to clear the image

    # check for packet rx
    packet = rfm69.receive()
    if packet is None:
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        npackets +=1 
        # Display the packet text and rssi
        #display.fill(0)
        packet_text = str(packet, "utf-8")
        datastr += packet_text+'\n'
        display.text('RX: ', 0, 0, 1)
        display.text(packet_text, 25, 0, 1)
        display.text("%f"%(npackets/(time.time()-t0)), 0, 8, 1)
        #time.sleep(.001)
        print(npackets,npackets/(time.time()-t0))
    display.show()
    time.sleep(0.005)
    display.fill(0)
    
    # check FLAG conditions
    if not btnA.value:
        # Check Button A
        FLAG = True
        print(datastr)
