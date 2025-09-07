# import json
# import ssl
# import paho.mqtt.client as mqtt
# from django.core.management.base import BaseCommand
# from emissions.models import Emissions

# BROKER = "57652ef3c2f34337b4fe5619db6f16b9.s1.eu.hivemq.cloud"
# PORT = 8883
# USERNAME = "CarbonTrack"
# PASSWORD = "@Carbontrack2025"
# TOPIC = "esp32/hello"

# class Command(BaseCommand):
#     help = "Run MQTT client and save incoming messages to database"

#     def handle(self, *args, **kwargs):
#         def on_connect(client, userdata, flags, rc, properties=None):
#             if rc == 0:
#                 self.stdout.write(self.style.SUCCESS("✅ Connected to broker"))
#                 client.subscribe(TOPIC, qos=1)
#             else:
#                 self.stdout.write(self.style.ERROR(f"❌ Connection failed: {rc}"))

#         def on_message(client, userdata, msg):
#             try:
#                 payload_str = msg.payload.decode("utf-8", errors="ignore").strip()
#                 data = json.loads(payload_str)

#                 if isinstance(data, dict):
#                     emission = Emissions.objects.create(
#                         device_id=data.get("device_id", "unknown"),
#                         emission_rate=data.get("co2_emission_kgs", 0.0)
#                     )
#                     emission.save()
#                     self.stdout.write(self.style.SUCCESS(
#                         f"Saved emission from {emission.device_id} - {emission.emission_rate} kg/s"
#                     ))
#                 else:
#                     self.stdout.write(f"Non-JSON message: {data}")

#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"Error: {e}"))

#         client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)
#         client.tls_set(tls_version=ssl.PROTOCOL_TLS)
#         client.username_pw_set(USERNAME, PASSWORD)
#         client.on_connect = on_connect
#         client.on_message = on_message

#         self.stdout.write("🔌 Connecting to broker...")
#         client.connect(BROKER, PORT, keepalive=60)
#         client.loop_forever()
