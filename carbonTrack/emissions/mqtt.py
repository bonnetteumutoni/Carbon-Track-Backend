# import json
# import ssl
# import paho.mqtt.client as mqtt
# from django.db import transaction
# from emissions.models import Emissions

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
#             with transaction.atomic():
#                 Emissions.objects.update_or_create(
#                     device_id=data.get('device_id', 'N/A'),
#                     defaults={'emission_rate': float(data.get('co2_emission_kgs', 0.0))}
#                 )
#             print(f"Saved emissions for device {data.get('device_id', 'N/A')}")
#         else:
#             print("Received data is not a dictionary:", data)
#     except Exception as e:
#         print(f"Error processing MQTT message: {e}")

# client = mqtt.Client(protocol=mqtt.MQTTv5)
# client.tls_set(tls_version=ssl.PROTOCOL_TLS)  
# client.username_pw_set(USERNAME, PASSWORD)
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(BROKER, PORT, keepalive=60)
# client.loop_start()


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
#             # Import inside function to avoid startup errors
#             from .models import Emissions

#             device_id = data.get('device_id', 'N/A')
#             emission_rate = float(data.get('co2_emission_kgs', 0.0))

#             # Update or create without filtering on emission_rate to allow same values
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
#     client.loop_start()  # non-blocking loop in another thread
