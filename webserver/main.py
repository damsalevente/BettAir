import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap


eventlet.monkey_patch()

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

data_from_mq   = ""
import requests

"""
Configure credentials BIG TODO into ENV FILE
"""
influx_cloud_url = "titkos"
influx_cloud_token = "titkos"
bucket = 'mybucket'
org = '18d7dd6618fbcd6d'


@app.route('/')
def index():
    return "<h1>Hello world</h1>"

@app.route('/mqtt')
def mqtt_latest():
    data = data_from_mq
    return render_template("index.html",data = data)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data_from_mq = message.payload.decode()
    data_dict = json.loads(data_from_mq)
    payload_for_influx = '{}/api/v2/write?org={}&bucket={}&precision=s'.format(influx_cloud_url, org,bucket)
    header = "--headers Authorization: Token {}".format(influx_cloud_token)
    data = '--data-raw mem,host=host1 temperature={} {}'.format(data_dict['temperature'], 83)
    requests.post(payload_for_influx+header+data)
    print(data_dict)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':
    mqtt.subscribe("/topic/bettair")
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
