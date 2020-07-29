#include <SPI.h>
#include <Wire.h>
#include <RH_RF69.h>          // RFM
#include <Adafruit_GFX.h>     // OLED
#include <Adafruit_SSD1306.h> // OLED
#include <RHReliableDatagram.h>
#include <avr/dtostrf.h>

// RFM
#define RF69_FREQ 915.0
#define RFM69_CS  8
#define RFM69_INT 3
#define RFM69_RST 4
#define LED       13

// Thermistor
#define THERMISTORPIN A0          // which analog pin to connect
#define THERMISTORNOMINAL 10000   // resistance at 25 degrees C
#define TEMPERATURENOMINAL 25     // temp. for nominal resistance (almost always 25 C)
#define NUMSAMPLES 5              // how many samples to take and average, more takes longer, but is more 'smooth'
#define BCOEFFICIENT 3950         // The beta coefficient of the thermistor (usually 3000-4000)
#define SERIESRESISTOR 10000      // the value of the 'other' resistor

RH_RF69 rf69(RFM69_CS, RFM69_INT);
int samples[NUMSAMPLES];

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(1); }
  analogReference(AR_EXTERNAL);

  Serial.println("Temperature Sensor 1!");
  Serial.println();

  pinMode(LED, OUTPUT); // do you need this?

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

float temp () {
  uint8_t i;
  float average;

  // take N samples in a row, with a slight delay
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(THERMISTORPIN);
   delay(10);
  }

  // average all the samples out
  average = 0;
  for (i=0; i< NUMSAMPLES; i++) {
     average += samples[i];
  }
  average /= NUMSAMPLES;

  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;

  float steinhart;
  steinhart = average / THERMISTORNOMINAL;     // (R/Ro)
  steinhart = log(steinhart);                  // ln(R/Ro)
  steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  steinhart = 1.0 / steinhart;                 // Invert
  steinhart -= 273.15;                         // convert to C

  return steinhart;

}

void loop()
{
  delay(1000);  // Wait 1 second between transmits, could also 'sleep' here!

  char datapacket[20]; // Buffer big enough for 7-character float, can send ~40/50 characters
  dtostrf(temp (), 6, 2, datapacket); // Leave room for too large numbers!

  char comma[2] = ","; // 2 bc it's null-terminated
  strcat(datapacket, comma);

  Serial.print("Sending data: "); Serial.println(datapacket);

  // Send a message!
  rf69.send((uint8_t *)datapacket, strlen(datapacket));
  rf69.waitPacketSent();

}
