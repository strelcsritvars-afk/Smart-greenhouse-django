#include <WiFi.h>
#include <HTTPClient.h> //For sending json
#include <ArduinoJson.h> //Requires package from librarymanager
#include "config.h" //Using config.h similiar to .env, don't store your passwords in code
#include "DHT.h" //Library for dht22 sensor, requires package from librarymanager
#include "LiquidCrystal_I2C.h" //Library for LCD 16x2 I2C, requires package from librarymanager
#include "Wire.h"
#include "time.h" 

#define moistureSensor 32
#define DHT22Sensor 4
#define DHTType DHT22

LiquidCrystal_I2C lcd(0x27, 16, 2); //lcd settings, adress, rows, columns

//Calibration values for moisture sensor
const int airValue = 2500; /// Calibrated
const int waterValue = 500; // Calibrated

//Setting up datetime
const char* ntpServer = "pool.ntp.org"; //Using UTC, for timezones need to add offset to following variables
const int gmtOffset_sec = 0;
const int daylightOffset_sec = 0;
struct tm timeinfo;

//Setting up DHT

DHT dht(DHT22Sensor, DHTType);

//Variables

int rawMoistureValue = 0;
int moistureValue = 0;
int humidity = 0;
int temperature = 0;
int lastSentHour = -1;
String lastSentTime = "";

void checkTime() //Function to check time
{
  struct tm timeinfo;
  if(!checkTime(&timeinfo))
  {
    Serial.println("Failed to retrive time");
    return String("Error");
  }
  return String(timeinfo.tm_hour) + ":" + String(timeinfo.tm_min) 
}

void displayData() //Function to display data on LCD
{
  lcd.clear();
  lcd.print("Hum: " + String(humidity) + "%");
  lcd.setCursor(0,1);
  lcd.print("Temp: " + String(temperature) + "C*");
}

void sendPayload() //function to create and send json
{
    //Preparing payload
  if (WiFi.status() == WL_CONNECTED)
{
    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");
    
    //json

    JsonDocument doc;
    doc["device"] = DEVICE_ID; 
    doc["soil_humidity"] = moistureValue;
    doc["air_humidity"] = humidity;
    doc["air_temperature"] = temperature;

    String jsonPayload;
    serializeJson(doc, jsonPayload);

    Serial.println("Sending json: " + jsonPayload);

    int httpResponse = http.POST(jsonPayload);

    if (httpResponse > 0) 
    {
      Serial.printf("HTTP Response code: %d\n", httpResponse);
      Serial.println("Response: " + http.getString());

    } 
    else 
    {
      Serial.printf("Error: %s\n", http.errorToString(httpResponse).c_str());
    }
    
    http.end();
  }

  else
  {
    Serial.println("No connection");
  }
}

void setup()
{
  Serial.begin(115200);

  lcd.init();
  lcd.backlight();
  delay(1000);
  lcd.setCursor(0,0);

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  lcd.print("Connection");
  lcd.setCursor(0,1);
  lcd.print("In progress");

  while(WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi Connected!");

  lcd.clear();
  lcd.print("Wifi connected!");
  delay(2000);
  lcd.clear();

  dht.begin();

  //Moisture sensor range
  analogSetAttenuation(ADC_11db);

  //Syncing time with NTP server
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

}

  void loop()
  {

    rawMoistureValue = analogRead(moistureSensor);
    Serial.println(rawMoistureValue); //testing purposes
    moistureValue = map(rawMoistureValue, waterValue, airValue, 0, 100); //More voltage means more moisture
    moistureValue = constrain(moistureValue,0,100);
    humidity = dht.readHumidity();
    temperature = dht.readTemperature(); //dht22.readTemperature(True) reads temperature in Farenheit
    
    struct tm timeinfo;

    displayData();

    delay(10000);

    if (checkTime(&timeinfo))
    {
      int current_hour = timeinfo.tm_hour;

      if (current_hour != last_sent)
      {
        lcd.clear();

        lcd.print("Sending data");
        sendPayload();
        last_sent = current_hour;
        delay(2000);
        lcd.clear();

        lcd.print("Data sent");
        delay(2000);
        lcd.clear();
      }
    }

    delay(2000);

    displayData();

    delay(10000);

  }
