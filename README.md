# SIC Technical Assignment 1

## Requirements
- **Hardware**: ESP32, Breadboard, Jumper wires, Micro USB cable, DHT11 Sensor
- **Software**: Arduino IDE, Python 3.x, Flask (`pip install flask`)

## Setup

### Arduino IDE
1. Install ESP32 Board Package:
   - Add URL: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
   - Install `esp32` in Boards Manager.
2. Install Libraries:
   - `DHT sensor library` by Adafruit
   - `Adafruit Unified Sensor`

### Python
- Install Flask: `pip install flask`

## Arduino Code

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11

const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";
const char* serverName = "http://192.168.18.65:5000/";

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  dht.begin();
}

void loop() {
  if ((WiFi.status() == WL_CONNECTED)) {
    HTTPClient http;
    http.begin(serverName);

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    String postData = "temperature=" + String(t) + "&humidity=" + String(h);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }
  
  delay(20000);
}
```

## Python Server
- Create flask server:
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    temperature = request.form.get('temperature')
    humidity = request.form.get('humidity')
    print(f"Received Temperature: {temperature} °C, Humidity: {humidity} %")
    return "Data received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Running
1. Run Flask Server:
```sh
python server.py
```
2. Upload Code to ESP32 via Arduino IDE.
3. Open Serial Monitor at 115200 baud rate to view connection status and sensor data.
5. Check the Flask Server
On your local server (running the Flask application), you should see the temperature and humidity data being printed in the terminal where you started the server, like this:
```yaml
Received Temperature: 25.00 °C, Humidity: 60.00 %
```
