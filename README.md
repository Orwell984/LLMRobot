# LLMRobot

//Install Raspbian

// Connect via SSH
ssh javier@my_ip

//Update the packages
sudo apt update
sudo apt upgrade -y

//Instal g++ (already came installed)
sudo apt install g++ -y
"Verification": g++ --version

//Install python3 (already came installed)
sudo apt install python3 .y
"Verification": python3 --version

//Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
//Iniciate the service of Ollama
sudo systemctl start ollama
sudo systemctl enable ollama

//Install llama 3.2 1B
ollama pull llama3.2:1b
ollama run llama3.2:1b
/exit

//Make the AI respond in JSON
nano Modelfile

FROM llama3.2:1b

SYSTEM """
You are an AI assistant.
Always respond ONLY in valid JSON with the following structure:

{
  "question": "...",
  "reasoning": "...",
  "answer": "..."
}
"""


ollama create llama-json -f Modelfile
ollama run llama-json
