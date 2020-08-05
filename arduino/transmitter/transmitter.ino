#include <SPI.h>
#include <RH_RF69.h>
#include <RHReliableDatagram.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32

// OLED
#define OLED_RESET 4
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Themistor
#define THERMISTORPIN       A0 
#define THERMISTORNOMINAL   10000 
#define TEMPERATURENOMINAL  25
#define NUMSAMPLES          5
#define BCOEFFICIENT        3950
#define SERIESRESISTOR      10000 
int samples[NUMSAMPLES];

// RFM
#define RF69_FREQ 915.0
#define RFM69_CS  8
#define RFM69_INT 3
#define RFM69_RST 4

#define RF69_FREQ 915.0

#define DEST_ADDRESS   1
#define MY_ADDRESS     2

#define RFM69_CS      8
#define RFM69_INT     3
#define RFM69_RST     4
#define LED           13

RH_RF69 rf69(RFM69_CS, RFM69_INT);
RHReliableDatagram rf69_manager(rf69, MY_ADDRESS);

void setup() 
{
  Serial.begin(115200);

  analogReference(AR_EXTERNAL);               // Thermistor

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // OLED
  display.display();
  delay(2000);

  pinMode(LED, OUTPUT);     
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);

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

uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
uint8_t data[] = "  OK";

void loop() {
  delay(1000);

  float thermTemp = getTemp();

  const int capacity = JSON_OBJECT_SIZE(3);
  StaticJsonDocument<capacity> data;
  
  data["name"] = "temp_sensor_1";
  data["value"] = thermTemp;
  data["unit"] = "C";

  char packet[128];
  serializeJson(data, packet);
  
  Serial.print("Sending "); Serial.println(packet);
  
  if (rf69_manager.sendtoWait((uint8_t *)packet, strlen(packet), DEST_ADDRESS)) {
    uint8_t len = sizeof(buf);
    uint8_t from;   
    if (rf69_manager.recvfromAckTimeout(buf, &len, 2000, &from)) {
      buf[len] = 0;
      
      Serial.print("Got reply from #"); Serial.print(from);
      Serial.print(" [RSSI :");
      Serial.print(rf69.lastRssi());
      Serial.print("] : ");
      Serial.println((char*)buf);     
      Blink(LED, 40, 3); //blink LED 3 times, 40ms between blinks
    } else {
      Serial.println("No reply, is anyone listening?");
    }
  } else {
    Serial.println("Sending failed (no ack)");
  }
}

float getTemp() 
{
  uint8_t i;
  float average;
 
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(THERMISTORPIN);
   delay(10);
  }
  
  average = 0;
  for (i=0; i< NUMSAMPLES; i++) {
     average += samples[i];
  }
  average /= NUMSAMPLES;
  
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;
  
  float thermTemp;
  thermTemp = average / THERMISTORNOMINAL;     
  thermTemp = log(thermTemp);                  
  thermTemp /= BCOEFFICIENT;
  thermTemp += 1.0 / (TEMPERATURENOMINAL + 273.15);
  thermTemp = 1.0 / thermTemp;
  thermTemp -= 273.15;

  return thermTemp;
}

void prepareDisplay() 
{
  display.clearDisplay();
  display.setTextSize(1.5);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
}

void Blink(byte PIN, byte DELAY_MS, byte loops) {
  for (byte i=0; i<loops; i++)  {
    digitalWrite(PIN,HIGH);
    delay(DELAY_MS);
    digitalWrite(PIN,LOW);
    delay(DELAY_MS);
  }
}
