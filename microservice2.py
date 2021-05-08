import cherrypy
from cherrypy.process.plugins import Daemonizer, PIDFile
import random
import sys

port = 8002

class Root:
  @cherrypy.expose
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def index(self) -> str:
      params = cherrypy.request.json
      content = params["content"]
      print("content " , content)
      try:
        result = {"server":str(port), "content":str(random.randint(0,int(content)))}
      except ValueError:
        result = {"server":str(port), "content":"error: Invalid number"}
      
      return result


def run():
  cherrypy.config.update({
      "environment": "production",
      "log.screen": True,
      "server.socket_port": port,
  })
  PIDFile(cherrypy.engine, 'server'+str(port)+'.pid').subscribe()
  Daemonizer(cherrypy.engine).subscribe()
  cherrypy.quickstart(Root())


if __name__ == '__main__':
  if(len(sys.argv) != 2):
    print("Please specify port: python server _portnumber_")
  port = int(sys.argv[1])
  run()
