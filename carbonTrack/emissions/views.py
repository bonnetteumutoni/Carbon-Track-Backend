import threading
import queue
import json
from django.db import transaction
from rest_framework import viewsets
from .models import Emissions
from .serializers import EmissionsSerializer

# Queue for batching MQTT messages
message_queue = queue.Queue()
stop_event = threading.Event()

# Batch processor to save emissions
def process_queue():
    while not stop_event.is_set():
        try:
            messages = []
            # Collect messages for 1 second
            while True:
                msg = message_queue.get_nowait()
                messages.append(msg)
        except queue.Empty:
            if messages:
                with transaction.atomic():
                    for device_id, value in messages:
                        emission = Emissions(device_id=device_id, value=value)
                        emission.save()
                    print(f"Saved {len(messages)} emissions")
        stop_event.wait(1)  # Wait 1 second before next batch

# MQTT on_message handler
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode('utf-8'))
        device_id = payload.get('device_id', 'ESP32-000000000000')
        value = float(payload.get('value', 0))
        message_queue.put((device_id, value))
        print(f"Queued emission for {device_id}")
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Start the queue processor thread (add this to your MQTT client setup)
queue_thread = threading.Thread(target=process_queue)
queue_thread.start()

# Existing ViewSet (ensure it’s present)
class EmissionsViewSet(viewsets.ModelViewSet):
    queryset = Emissions.objects.all()
    serializer_class = EmissionsSerializer

# Your existing views (do not remove)
class RegisterUserView:
    pass  # Keep your implementation

class LoginView:
    pass  # Keep your implementation