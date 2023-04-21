# import zerorpc
#
#
# class StreamingRPC(object):
#     @zerorpc.stream
#     def streaming_range(self, fr, to, step):
#         return range(fr, to, step)
#
#
# s = zerorpc.Server(StreamingRPC())
# s.bind("tcp://0.0.0.0:4242")
# s.run()
#
#
# class ExceptionalRPC(object):
#     def bad(self):
#         raise Exception(":P")
#
#
# s = zerorpc.Server(ExceptionalRPC())
# s.bind("tcp://0.0.0.0:4242")
# s.run()

from flask import Flask, request, make_response

app = Flask(__name__)


# Define the handler function for incoming requests
@app.route('/process_data', methods=['POST'])
def process_data():
    # Get the data from the request
    data = request.get_data()
    # Process the data
    processed_data = data.upper()
    # Create a response with the processed data
    response = make_response(processed_data)
    # Set the content type of the response to plain text
    response.headers['Content-Type'] = 'text/plain'
    return response


# Run the server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
