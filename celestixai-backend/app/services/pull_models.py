from app.core.config import OLLAMA_SERVER_URL
from ollama import Client

client = Client(host=OLLAMA_SERVER_URL)


def pull_model(model_name: str):
    global client
    try:
        return client.pull(model_name)
    except Exception as e:
        raise FileNotFoundError("Model not found", e)
