import time
import BaseHTTPServer

HOST_NAME = '192.168.4.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.
value = ""
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
        global value
        print "GET request,\nPath: ", str(s.path),"\nHeaders:\n", str(s.headers), "\n\nBody:\n",value, "\n"
        
        s.wfile.write(value)
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
    def do_POST(s):
        content_length = int(s.headers['Content-Length']) # <--- Gets the size of data
        post_data = s.rfile.read(content_length) # <--- Gets the data itself
        print "POST request,\nPath: ",str(s.path),"\nHeaders:\n", str(s.headers), "\n\nBody:\n", post_data.decode('utf-8'), "\n"
        global value
        value = post_data.decode('utf-8')
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