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
