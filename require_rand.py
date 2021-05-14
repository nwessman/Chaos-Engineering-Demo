import cherrypy
from cherrypy.process.plugins import Daemonizer, PIDFile
import requests

class Root:
  @cherrypy.expose
  def index(self, payload):
    # payload is sent to the server by requesting http://localhost:8001/index/payload
    # payload should be a positive integer number
    print("content: ", payload)

    server_list = ["http://localhost:8002/","http://localhost:8003/"]
    
    # Sends a post request asking for a random number between 0 and payload
    # Tries the servers in the order they are in server_list
    for server in server_list:
      try:
        r = requests.post(server, timeout=(2,2), json={"content":payload})
        if(r.status_code == 200):
          break 
      except:
        continue

    if(r.status_code != 200):
      raise cherrypy.HTTPError(500, r.text)

    cherrypy.response.headers["Content-Type"] = "text/plain"
    return "response from service: {}: {}\n".format(r.json()["server"],r.json()["content"])

  
def main():
  # Setting up and running the server in a background process
  cherrypy.config.update({
    "environment": "production",
    "log.screen": True,
    "server.socket_port": 8001
  })
  PIDFile(cherrypy.engine, "require_rand.pid").subscribe()
  Daemonizer(cherrypy.engine).subscribe()
  cherrypy.quickstart(Root())

if __name__ == '__main__':
  main()