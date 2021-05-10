import cherrypy
from cherrypy.process.plugins import Daemonizer, PIDFile
import random
import sys

port = 8002
name = "server"

class Root:
  @cherrypy.expose
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def index(self) -> str:
      params = cherrypy.request.json
      content = params["content"]
      try:
        result = {"server":name+" ("+str(port)+")", "content":str(random.randint(0,int(content)))}
      except ValueError:
        result = {"server":name+" ("+str(port)+")", "content":"error: Invalid number"}
      
      return result


def run():
  cherrypy.config.update({
      "environment": "production",
      "log.screen": True,
      "server.socket_port": port,
  })
  PIDFile(cherrypy.engine, name+'.pid').subscribe()
  Daemonizer(cherrypy.engine).subscribe()
  cherrypy.quickstart(Root())


if __name__ == '__main__':
  if(len(sys.argv) != 3):
    print("Please specify port and name of server: python server _portnumber_ _servername_")
  port = int(sys.argv[1])
  name = sys.argv[2]
  run()
