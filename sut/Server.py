import sys, os
from BaseHTTPServer import BaseHTTPRequestHandler
import SocketServer
import json
import time
from do_load import do_load

hostName = '0.0.0.0'
hostPort = int(os.getenv('PORT'))
print(str(hostName)+":"+str(hostPort))

# This is a python web server - it must have the environment variable PORT set on the machine it is running on.
# e.g. PORT=8080
#
# If the web server receives a POST request of data=nnn it wil return nnn
# If it receives a POST of {"data": nnnnn} then it'll return {"returned": nnnnn}
# If it receives any other name, e.g. value=nnnnn, then it'll return -1
# (Where nnnn represents an integer number)
class Server(BaseHTTPRequestHandler):

    def __init__(self,request,client_addres,server):
        BaseHTTPRequestHandler.__init__(self,request,client_addres,server)
        self.request_id = ''

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        with open(self.path.strip("/"), 'r') as file:
            self.wfile.write(file.read().encode('UTF-8'))

    def do_POST(self):
        self._set_response()
        content_length = int(self.headers['Content-length'])
        post_data = self.rfile.read(content_length)
        self._set_response()
        # default sleep time
        sleep = 5
        try:
            name = post_data.decode('utf-8').split("=")[0]
            val = post_data.decode('utf-8').split("=")[1]
            if name == "data":
                ret_val = "data=" + val
            else:
                ret_val = "data=-1"

        except IndexError:
            # must be JSON
            loaded = json.loads(post_data.decode('utf-8'))
            if 'runtime' and 'cores' in loaded.keys():
                print("***** Calling do_load.py *****")
                do_load(loaded['runtime'], loaded['cores'])
                json_ret_val = {"returned": loaded['runtime']}
            else:
               for x in loaded:
                    print("%s: %d" % (x, loaded[x]))
                    json_ret_val = {"returned": loaded[x]}
        ret_val = json.dumps(json_ret_val)
        print("Returning: "+ret_val)
        # put a pause in to make the test take a measurable length of time.
        time.sleep(sleep)
        self.wfile.write(ret_val.encode('UTF-8'))



try:
    svr = SocketServer.TCPServer((hostName, hostPort), Server)
    print("Web server running on: "+hostName+":"+str(hostPort))
    svr.serve_forever()
except KeyboardInterrupt:
    print("^C stopping web server...")
    svr.socket.close()

