#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> //Requires package from librarymanager
#include "config.h"


//!!!TESTING ONLY, WONT WORK WITH SENSORS, FOR USE UPLOAD esp32_node.ino

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi Connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");

    //Test data generation
    int fake_soil_humidity = random(30, 80);    // Random soil % between 30 and 80
    int fake_air_humidity = random(40, 70);     // Random air % between 40 and 70
    int fake_air_temperature = random(18, 28);  // Random temp between 18°C and 28°C

    //JSON
    
    StaticJsonDocument<200> doc;
    doc["device"] = DEVICE_ID; 
    doc["soil_humidity"] = fake_soil_humidity;
    doc["air_humidity"] = fake_air_humidity;
    doc["air_temperature"] = fake_air_temperature;

    String jsonPayload;
    serializeJson(doc, jsonPayload);

    Serial.println("Sending test payload: " + jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.printf("HTTP Response code: %d\n", httpResponseCode);
      Serial.println("Response: " + http.getString());
    } else {
      Serial.printf("Error: %s\n", http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  }

  delay(10000); // Send test ping every 10 seconds
}