import time
import numpy as np
import BaseHTTPServer
from model import LSTMModel

HOST_NAME = '192.168.4.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.
value = np.zeros(2)
model = LSTMModel("Model2.json", "Model2.h5")
start_time = time.time()
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        global model
        global value
        predicted = model.get_prediction(value)
        print "Predicted: ", predicted[0], ", ", predicted[1]
        if time.time() >= predicted[1]:
            s.wfile.write(predicted[0])
            print "GET request,\nPath: ", str(s.path),"\nHeaders:\n", str(s.headers), "\n\nBody:\n",predicted[0], "\n"
        else:
            s.wfile.write(value[0])
            print "GET request,\nPath: ", str(s.path),"\nHeaders:\n", str(s.headers), "\n\nBody:\n",value[0], "\n"
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
    def do_POST(s):
        content_length = int(s.headers['Content-Length']) # <--- Gets the size of data
        post_data = s.rfile.read(content_length) # <--- Gets the data itself
        print "POST request,\nPath: ",str(s.path),"\nHeaders:\n", str(s.headers), "\n\nBody:\n", post_data.decode('utf-8'), "\n"
        global value
        global start_time
        value_str = post_data.decode('utf-8')
        value[0] = int(value_str)
        value[1] = time.time() - start_time
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        s.wfile.write("Success")
if __name__ == '__main__':
    
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print (time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))