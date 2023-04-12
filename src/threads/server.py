import time
import os
from PyQt5.QtCore import QThread
from http.server import BaseHTTPRequestHandler, HTTPServer

import http.server
import socketserver


import asyncio
from websockets.server import serve

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):    
  def do_GET(self):
    print(self.path)
    # ~ self.send_response(201)
    # ~ self.send_header("Content-type", "text/html")
    # ~ self.end_headers()
    # ~ if self.path == '/':
      # ~ self.path = "/home/pi/weather_station_data"
      # ~ self.path = os.path.abspath("/home/pi/weather_station_data")
      # ~ self.path = 'mywebpage.html'
    return http.server.SimpleHTTPRequestHandler.do_GET(self)

class MyServer(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("<html><head><title>Pi Weather Station</title></head>", "utf-8"))
    self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
    self.wfile.write(bytes("<body>", "utf-8"))
    mypath = os.path.abspath("/home/pi/weather_station_data")
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # ~ print(onlyfiles)
    for file_name in onlyfiles:
      print(file_name)
    # ~ <a href="/images/myw3schoolsimage.jpg" download>
      self.wfile.write(bytes("<a href='%s' download>Download</a>" % file_name, "utf-8"))
    self.wfile.write(bytes("<p>Weather station data here.</p>", "utf-8"))
    self.wfile.write(bytes("</body></html>", "utf-8"))

class ServerThread(QThread):
  def __init__(self):
    super(ServerThread, self).__init__()    

    self.host_name = "10.42.0.1"
    self.server_port = 8080
    self.path = os.path.abspath("/home/pi/weather_station_data")
    
    # ~ web_dir = os.path.join()
    os.chdir(self.path)
    
    ###
    # ~ self.handler = http.server.SimpleHTTPRequestHandler
    self.handler = MyHttpRequestHandler
    ###
    
    
    # ~ self.host_name = "localhost"
    # ~ self.server_port = 8765
    
    # ~ self.web_server = HTTPServer((self.host_name, self.server_port), MyServer)
    # ~ print("Server started http://%s:%s" % (self.host_name, self.server_port))
    self.start()
    
  async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

  async def main():
    async with serve(echo, self.host_name, self.server_port):
        await asyncio.Future()  # run forever
  
  def run(self):
    try:
      # ~ asyncio.run(self.main())
      
      # ~ self.web_server.serve_forever()
      
      ###
      
      with socketserver.TCPServer(("", self.server_port), self.handler) as httpd:
        print("Server started at localhost:" + str(self.server_port))
        httpd.serve_forever()
      
      ###
      
    except:
      print("web server error")
      
    # ~ web_server.server_close()
    # ~ server_address = (self.host_name, self.server_port)
    # ~ httpd = server_class(server_address, handler_class)
    # ~ httpd.serve_forever()
   



# ~ if __name__ == "__main__":        
    # ~ webServer = HTTPServer((hostName, serverPort), MyServer)
    # ~ print("Server started http://%s:%s" % (hostName, serverPort))

    # ~ try:
        # ~ webServer.serve_forever()
    # ~ except KeyboardInterrupt:
        # ~ pass

    # ~ webServer.server_close()
    # ~ print("Server stopped.")
