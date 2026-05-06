import json
import requests
from paho.mqtt import client as mqtt_client

# MQTT SPECIFICATIONS 

BROKER_IP = "10.21.60.231"
BROKER_PORT = 1883

REQUEST_TOPIC = "robot/llm/request"
RESPONSE_TOPIC = "robot/llm/response"

# OLLAMA SETTINGS 

OLLAMA_URL = "http://localhost:11434/api/generate"

# Use custom JSON model if installed
MODEL_NAME = "llama-json"

# Fallback model:
# MODEL_NAME = "llama3.2:1b"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[+] Connected to MQTT Broker")
        client.subscribe(REQUEST_TOPIC)
        print(f"[+] Listening on topic: {REQUEST_TOPIC}")
    else:
        print(f"[!] Failed to connect. Return code: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8", errors="replace").strip()

        print(f"[MQTT → LLM]: {payload}")

        
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": payload,
                "stream": False
            }
        )

        
        data = response.json()

        raw_response = data.get("response", "").strip()

        if not raw_response:
            print("[!] Empty response from Ollama")
            return

        
        try:
            parsed = json.loads(raw_response)

            answer = parsed.get("answer", "").strip()

            if not answer:
                answer = raw_response

        except json.JSONDecodeError:
            
            answer = raw_response

        print(f"[LLM → MQTT]: {answer}")

        
        client.publish(
            RESPONSE_TOPIC,
            answer
        )

    except Exception as e:
        print(f"[ERROR]: {e}")

# MQTT CLIENT 

client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, BROKER_PORT, 60)

print("===================================")
print("      LLM BRIDGE STARTED")
print("===================================")

client.loop_forever()
