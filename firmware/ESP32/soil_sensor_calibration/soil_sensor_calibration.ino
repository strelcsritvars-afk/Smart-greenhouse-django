#define moistureSensor 32

void setup()
{
  Serial.begin(115200);
  analogSetAttenuation(ADC_11db);
}

void loop()
{
  int rawMoistureValue = analogRead(moistureSensor);
  Serial.print("Raw Moisture Value: ");
  Serial.println(rawMoistureValue);
  delay(1000);
}