// DHT
#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN 12
#define DHTTYPE DHT22

// Themistor
#define THERMISTORPIN A0 
#define THERMISTORNOMINAL 10000 
#define TEMPERATURENOMINAL 25
#define NUMSAMPLES 5
#define BCOEFFICIENT 3950
#define SERIESRESISTOR 10000 
int samples[NUMSAMPLES];

// OLED Display
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32

#define OLED_RESET 4
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  
  analogReference(AR_EXTERNAL);               // Thermistor
  dht.begin();                                // DHT
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // OLED
  display.display();
  delay(2000);
  display.clearDisplay();
  
}

void loop() {
  delay(1000);

  // Thermistor Calculations
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
  
  float dhtHumidity = dht.readHumidity();         // DHT Humidity
  float dhtTempC = dht.readTemperature();         // DHT Temperature (C)
  float dhtTempF = dht.readTemperature(true);     // DHT Temperature (F)

  if (isnan(dhtHumidity) || isnan(dhtHumidity) || isnan(dhtHumidity)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Thermistor Output
//  Serial.print("Thermistor: ");
//  Serial.print(thermTemp);
//  Serial.print("\n");

  // Output in OLED Display
  display.clearDisplay();

  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.print(F("Humidity: "));
  display.println(dhtHumidity);
  display.print(F("Temperature: "));
  display.println(dhtTempC);

  display.display();
}