import json
import paho.mqtt.client as mqtt
import ssl
import requests  

BROKER = "57652ef3c2f34337b4fe5619db6f16b9.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "CarbonTrack"
PASSWORD = "@Carbontrack2025"
TOPIC = "esp32/hello"
API_URL = "http://127.0.0.1:8000/api/emissions/"  

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(TOPIC, qos=1) 
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8", errors="ignore").strip()
        data = json.loads(payload_str)
        print(f"\nTopic: {msg.topic} QoS: {msg.qos}")
        if isinstance(data, dict):
            def safe_get(key):
                val = data.get(key)
                return val if val is not None else "N/A"

            print(f"Device ID   : {safe_get('device_id')}")
            print(f"Uptime      : {safe_get('uptime_seconds')} s")
            print(f"WiFi RSSI   : {safe_get('wifi_rssi')} dBm")
            print(f"Heap Free   : {safe_get('free_heap')} bytes")
            print(f"CO2 Rate    : {safe_get('co2_emission_kgs')} kg/s")
            print("-----------------------------")

            
            api_payload = {
                "device_id": safe_get('device_id'),
                "emission_rate": safe_get('co2_emission_kgs') if safe_get('co2_emission_kgs') != "N/A" else 0.0
            }

            
            response = requests.post(API_URL, json=api_payload)
            if response.status_code == 201:
                print("Emission data successfully sent to API")
            else:
                print(f"Failed to send data to API: {response.status_code} - {response.text}")

        else:
            print(data)
    except json.JSONDecodeError:
        print(f"\nRaw message received on topic {msg.topic}: {payload_str}")
    except Exception as e:
        print(f"\nError decoding message on topic {msg.topic}: {e}")


client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()

# import paho.mqtt.client as mqtt
# import ssl
# import json

# BROKER = "57652ef3c2f34337b4fe5619db6f16b9.s1.eu.hivemq.cloud"
# PORT = 8883
# USERNAME = "CarbonTrack"
# PASSWORD = "@Carbontrack2025"
# TOPIC = "esp32/hello"


# def on_connect(client, userdata, flags, rc, properties=None):
#     if rc == 0:
#         print("Connected to MQTT broker")
#         client.subscribe(TOPIC, qos=1)
#     else:
#         print(f"Failed to connect with code {rc}")


# def on_message(client, userdata, msg):
#     payload_str = msg.payload.decode("utf-8", errors="ignore").strip()
#     try:
#         data = json.loads(payload_str)
#         if isinstance(data, dict):
#             from .models import Emissions
#             device_id = data.get('device_id', 'N/A')
#             emission_rate = float(data.get('co2_emission_kgs', 0.0))
#             Emissions.objects.update_or_create(
#                 device_id=device_id,
#                 defaults={'emission_rate': emission_rate}
#             )
#             print(f"Saved emissions for device {device_id}")
#     except Exception as e:
#         print(f"Error processing MQTT message: {e}")


# def mqtt_start_loop():
#     client = mqtt.Client(protocol=mqtt.MQTTv5)
#     client.tls_set(tls_version=ssl.PROTOCOL_TLS)
#     client.username_pw_set(USERNAME, PASSWORD)
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.connect(BROKER, PORT, keepalive=60)
#     client.loop_start() 

# import paho.mqtt.client as mqtt
# import ssl
# import json

# BROKER = "57652ef3c2f34337b4fe5619db6f16b9.s1.eu.hivemq.cloud"
# PORT = 8883
# USERNAME = "CarbonTrack"
# PASSWORD = "@Carbontrack2025"
# TOPIC = "esp32/hello"


# def on_connect(client, userdata, flags, rc, properties=None):
#     if rc == 0:
#         print("MQTT Connected")
#         client.subscribe(TOPIC, qos=1)
#     else:
#         print(f"MQTT Connection failed with code {rc}")


# def on_message(client, userdata, msg):
#     payload_str = msg.payload.decode("utf-8", errors="ignore").strip()
#     try:
#         data = json.loads(payload_str)
#         if isinstance(data, dict):
#             # Import inside the function to avoid startup errors
#             from .models import Emissions  

#             device_id = data.get('device_id', 'N/A')
#             emission_rate = float(data.get('co2_emission_kgs', 0.0))

#             # Update or create record in DB directly - no HTTP calls
#             Emissions.objects.update_or_create(
#                 device_id=device_id,
#                 defaults={'emission_rate': emission_rate}
#             )
#             print(f"Saved emissions for device {device_id}")
#     except Exception as e:
#         print(f"Error processing MQTT message: {e}")


# def start_mqtt():
#     client = mqtt.Client(protocol=mqtt.MQTTv5)
#     client.tls_set(tls_version=ssl.PROTOCOL_TLS)
#     client.username_pw_set(USERNAME, PASSWORD)
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.connect(BROKER, PORT, keepalive=60)
#     client.loop_start()  # non-blocking loop, runs in background thread
