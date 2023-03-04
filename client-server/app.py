import requests

# Define the data to send
data = b'Hello, server!'

# Send a POST request to the server
response = requests.post('http://127.0.0.1:5000/process_data', data=data)

# Print the response content
print(response.content.decode())