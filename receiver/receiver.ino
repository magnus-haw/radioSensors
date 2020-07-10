#include <SPI.h>
#include <Wire.h>
#include <RH_RF69.h>          // RFM
#include <Adafruit_GFX.h>     // OLED
#include <Adafruit_SSD1306.h> // OLED
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

RH_RF69 rf69(RFM69_CS, RFM69_INT);

void setup() 
{
  Serial.begin(115200);

  analogReference(AR_EXTERNAL);               // Thermistor

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // OLED
  display.display();
  delay(2000);

  pinMode(RFM69_RST, OUTPUT);                 // RFM
  digitalWrite(RFM69_RST, LOW);

  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);
  
  if (!rf69.init()) {
    prepareDisplay();
    display.setCursor(0,0);
    display.print("RFM69 radio init failed");
    while (1);
  }
  prepareDisplay();
  display.setCursor(0,0);
  display.print("RFM69 radio init OK!");

  
  if (!rf69.setFrequency(RF69_FREQ)) {
    prepareDisplay();
    display.setCursor(0,0);
    display.print("set frequency failed");
  }

  rf69.setTxPower(20, true);

  uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  rf69.setEncryptionKey(key);
}

void loop() 
{
  float thermTemp = getTemp();
  char str[16];
  snprintf(str, sizeof(str), "%.2f", thermTemp);
  rf69.send((uint8_t *)str, sizeof(thermTemp));
  rf69.waitPacketSent();
  prepareDisplay();
  display.print("Sent Temperature: ");
  display.println(str);
  display.display();
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
