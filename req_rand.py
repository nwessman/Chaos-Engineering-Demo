import cherrypy
from cherrypy.process.plugins import Daemonizer, PIDFile
import requests

class Root:
  @cherrypy.expose
  def index(self, payload):
    print("content: ", payload)

    server_list = ["http://localhost:8002/","http://localhost:8003/"]
    
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
    return "response from service {}: {}\n".format(r.json()["server"],r.json()["content"])

  
def main():
  cherrypy.config.update({
    "environment": "production",
    "log.screen": True,
    "server.socket_port": 8001
  })
  PIDFile(cherrypy.engine, "microservice1.pid").subscribe()
  Daemonizer(cherrypy.engine).subscribe()
  cherrypy.quickstart(Root())

if __name__ == '__main__':
  main()