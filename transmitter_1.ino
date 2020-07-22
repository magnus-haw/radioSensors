#include <SPI.h>
#include <Wire.h>
#include <ArduinoJson.h>
#include <RH_RF69.h>          // RFM
#include <Adafruit_GFX.h>     // OLED
#include <Adafruit_SSD1306.h> // OLED
#include <RHReliableDatagram.h>

// RFM
#define RF69_FREQ 915.0
#define RFM69_CS  8
#define RFM69_INT 3
#define RFM69_RST 4

RH_RF69 rf69(RFM69_CS, RFM69_INT);

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(1); }

  Serial.println("Test serial print 1.");
  Serial.println();

  pinMode(RFM69_RST, OUTPUT);                 // Manually prepare output pin
  digitalWrite(RFM69_RST, LOW);
  delay(10);
  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);

  if (!rf69.setFrequency(RF69_FREQ)) {
    Serial.println("Set frequency failed.");
  }
  Serial.println("Set frequency OK!");
  if (!rf69.init()) {
    Serial.println("RFM69 radio init failed");
    while (1);
  }
  Serial.println("RFM69 radio init OK!");

  rf69.setTxPower(20, true);
}

void loop()
{
  delay(5000);
  const int CAPACITY = JSON_OBJECT_SIZE(1); // only one pair (see below)
  StaticJsonDocument<CAPACITY> data;

  JsonObject object = data.to<JsonObject> (); // create an object, JsonObjects come in key-value pairs
  object["hello"] = "world"; // assigning pair

  char buf[128]; // creates buffer containing at most 128 bytes
  serializeJson(data, buf); // serialize the object and send the result to the buffer (like a loading pad)

  Serial.println("Sending packet!");

  rf69.send((uint8_t *)buf, sizeof(buf)); // send info!
  rf69.waitPacketSent(); // wait until done transmitting
}
