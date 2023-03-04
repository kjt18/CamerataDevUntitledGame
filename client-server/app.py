import requests

# Define the data to send
data = b'Hello, server!'

# Send a POST request to the server
response = requests.post('http://127.0.0.1:5000/process_data', data=data)

# Print the response content
print(response.content.decode())


# another way of implementing client-server connection, saving for future use
# import zerorpc
#
# c = zerorpc.Client()
# c.connect("tcp://127.0.0.1:4242")
#
# for item in c.streaming_range(10, 20, 2):
#     print(item)