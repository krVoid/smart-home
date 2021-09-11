from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json 
from random import randrange

hostName = "localhost"
serverPort = 8082

class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        print(self.path)
        if self.path == "/output/0/turn-on":
            print('start')
        elif self.path == "/output/0/turn-off":
            print('stop')
        elif self.path == "/output/1/set-value":
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length) 
            print('set value ', post_data)
        elif self.path == "/sensor/0/":
            humidity = randrange(25)
            print(humidity)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(str(humidity), 'utf-8'))
        elif self.path == "/sensor/1/":
            temperature = randrange(46)
            print(temperature)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(str(temperature), 'utf-8'))
    def do_GET(self):
        if self.path == "/register":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send the html message
            msg = {
                'outputs': [
                    {
                        'name': "Turn on/off",
                        'description': "",
                        'isBinary': True,
                        'outputId': 0
                    },
                    {
                        'name': "Set value",
                        'description': "",
                        'isBinary': False,
                        'outputId': 1,
                        'min': 0,
                        'max': 100
                    },
                ],
                'inputs': [
                    {
                        'name': "Humidity",
                        "description": "Return value from - to 25",
                        "inputId": 0
                    },
                    {
                        'name': "Temperature",
                        "description": "Return value from 0 to 46",
                        "inputId": 1
                    },
                ]
            }
            self.wfile.write(bytes(json.dumps(msg, ensure_ascii=False), 'utf-8'))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

# vac = Vacuum("192.168.0.213", "3678594b656933756f6b5161734e6661")
# vac.stop()
# vac.add_timer("30 18 * * *", 'start', None)
