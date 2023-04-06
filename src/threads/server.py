import time
from PyQt5.QtCore import QThread
from http.server import BaseHTTPRequestHandler, HTTPServer

import asyncio
from websockets.server import serve

class MyServer(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("<html><head><title>Pi Weather Station</title></head>", "utf-8"))
    self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
    self.wfile.write(bytes("<body>", "utf-8"))
    self.wfile.write(bytes("<p>Weather station data here.</p>", "utf-8"))
    self.wfile.write(bytes("</body></html>", "utf-8"))

class ServerThread(QThread):
  def __init__(self):
    super(ServerThread, self).__init__()    

    # ~ self.host_name = "10.42.0.1"
    # ~ self.server_port = 8080
    
    self.host_name = "localhost"
    self.server_port = 8765
    
    # ~ self.web_server = HTTPServer((self.host_name, self.server_port), MyServer)
    print("Server started http://%s:%s" % (self.host_name, self.server_port))
    self.start()
    
  async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

  async def main():
    async with serve(echo, self.host_name, self.server_port):
        await asyncio.Future()  # run forever
  
  def run(self):
    try:
      asyncio.run(self.main())
      # ~ self.web_server.serve_forever()
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
