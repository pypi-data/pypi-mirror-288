import requests

FLAMINIO_ENDPOINT = "http://169.229.48.114:8000/"
LOCAL_ENDPOINT = "http://localhost:8000/"

QUERY = "When is UC Berkeley founded?"

retrieval_response = requests.post(FLAMINIO_ENDPOINT + "retrieve", json={"query": QUERY})
print(retrieval_response.json())

chat_response = requests.post(FLAMINIO_ENDPOINT + "chat", json={"query": QUERY})
print(chat_response.json())