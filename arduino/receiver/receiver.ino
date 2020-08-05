#include <SPI.h>
#include <RH_RF69.h>
#include <RHReliableDatagram.h>
#include <Adafruit_GFX.h>     // OLED
#include <Adafruit_SSD1306.h> // OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32

#define RF69_FREQ 915.0
#define MY_ADDRESS     1

#define RFM69_CS      8
#define RFM69_INT     3
#define RFM69_RST     4
#define LED           13

RH_RF69 rf69(RFM69_CS, RFM69_INT);
RHReliableDatagram rf69_manager(rf69, MY_ADDRESS);

// OLED
#define OLED_RESET 4
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() 
{
  Serial.begin(115200);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // OLED
  display.display();
  delay(2000);

  pinMode(LED, OUTPUT);     
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);

  Serial.println("Feather Addressed RFM69 RX Test!");
  Serial.println();

  // manual reset
  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);
  
  if (!rf69_manager.init()) {
    Serial.println("RFM69 radio init failed");
    while (1);
  }
  Serial.println("RFM69 radio init OK!");
  
  if (!rf69.setFrequency(RF69_FREQ)) {
    Serial.println("setFrequency failed");
  }

  rf69.setTxPower(20, true);

  uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  rf69.setEncryptionKey(key);
  
  pinMode(LED, OUTPUT);

  Serial.print("RFM69 radio @");  Serial.print((int)RF69_FREQ);  Serial.println(" MHz");
}

uint8_t data[] = "OK";
uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];

void loop() {
  if (rf69_manager.available())
  {
    uint8_t len = sizeof(buf);
    uint8_t from;
    if (rf69_manager.recvfromAck(buf, &len, &from)) {
      buf[len] = 0;
      
      Serial.print("Got packet from #"); Serial.print(from);
      Serial.print(" [RSSI :");
      Serial.print(rf69.lastRssi());
      Serial.print("] : ");
      Serial.println((char*)buf);
      Blink(LED, 40, 3);

      if (!rf69_manager.sendtoWait(data, sizeof(data), from))
        Serial.println("Sending failed (no ack)");
    }
  }
}

void Blink(byte PIN, byte DELAY_MS, byte loops) {
  for (byte i=0; i<loops; i++)  {
    digitalWrite(PIN,HIGH);
    delay(DELAY_MS);
    digitalWrite(PIN,LOW);
    delay(DELAY_MS);
  }
}
