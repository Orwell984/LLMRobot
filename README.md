# LLM ROBOT SETUP GUIDE

First, update the Raspberry Pi packages:

sudo apt update
sudo apt upgrade -y

Install Python and pip:

sudo apt install python3 python3-pip -y

Verify Python installation:
python3 --version

Install the required Python libraries for MQTT communication and Ollama API requests:

pip install paho-mqtt requests

Install Ollama:

curl -fsSL https://ollama.com/install.sh | sh

Verify Ollama installation:

ollama --version

Start and enable the Ollama service:

sudo systemctl start ollama
sudo systemctl enable ollama

Install the Llama model:

ollama pull llama3.2:1b

Test the model:
ollama run llama3.2:1b

Type:

/exit

to exit the model.

Create a custom JSON model by creating a Modelfile:


nano Modelfile


Paste the following into the file:

FROM llama3.2:1b
System:
You are an AI assistant.

Always respond ONLY in valid JSON with the following structure:

{
  "question": "...",
  "reasoning": "...",
  "answer": "..."
}
"""


Save and exit the file.

Build the custom model:

ollama create llama-json -f Modelfile


Test the custom model:


ollama run llama-json


Place the file `llm_bridge.py` in the project folder.

Inside `llm_bridge.py`, set the broker IP address to match the Team 4 MQTT broker Raspberry Pi:

BROKER_IP = "10.21.60.231"

The LLM bridge subscribes to:

robot/llm/request


and publishes responses to:

robot/llm/response


Run the LLM bridge:

python3 llm_bridge.py


To test the system from another Raspberry Pi, publish a message:

mosquitto_pub -h 10.21.60.231 -t robot/llm/request -m "Hello"

If successful, Ollama will generate a response and publish it to:

robot/llm/response

Notes:

* Ollama runs locally on the Team 2 Raspberry Pi.
* The MQTT broker runs on the Team 4 Raspberry Pi.
* All Raspberry Pis must be connected to the same network.
* All devices must use the same broker IP address.
