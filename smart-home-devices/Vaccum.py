from miio import Vacuum, vacuum
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json 
hostName = "localhost"
serverPort = 8081

class MyServer(BaseHTTPRequestHandler):
    vacuum = Vacuum("192.168.0.213", "3678594b656933756f6b5161734e6661")
    def do_POST(self):
        print(self.path)
        if self.path == "/output/0/turn-on":
            print('start')
            self.vacuum.resume_or_start()
        elif self.path == "/output/0/turn-off":
            print('stop')
            self.vacuum.pause() 
        elif self.path == "/output/1/turn-on":
            self.vacuum.home()
        elif self.path == "/output/2/set-value":
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length) 
            self.vacuum.set_sound_volume(int(post_data))
        elif self.path == "/output/3/set-value":
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length) 
            takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
            self.vacuum.set_fan_speed(takeClosest(int(post_data), [38, 60 ,77]))

    def do_GET(self):
        print(self.path)
        if self.path == "/0/turn-on":
            self.vacuum.resume_or_start()
        elif self.path == "/0/turn-off":
            self.vacuum.pause() 
        elif self.path == "/register":
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
                        'name': "Return to home",
                        'description': "",
                        'isBinary': False,
                        'outputId': 1
                    },
                    {
                        'name': "Set sound volume",
                        'description': "",
                        'isBinary': False,
                        'outputId': 2,
                        'min': 0,
                        'max': 100
                    },
                    {
                        'name': "Set fan speed",
                        'description': "Set 38, 60 or 77",
                        'isBinary': False,
                        'outputId': 3,
                        'min': 38,
                        'max': 77
                    }
                ],
                'inputs': []
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
