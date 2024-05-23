from gradio_client import Client

client = Client("https://64c259e8818140638f.gradio.live/")
result = client.predict(
		message="Hello!!",
		api_name="/chat"
)
print(result)