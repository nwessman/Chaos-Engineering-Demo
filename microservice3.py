import cherrypy
from cherrypy.process.plugins import Daemonizer, PIDFile
import random


class Root:
  @cherrypy.expose
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def index(self) -> str:
      params = cherrypy.request.json
      content = params["content"]
      print("content " , content)
      try:
        result = {"server":"2", "content":str(random.randint(0,int(content)))}
      except ValueError:
        result = {"server":"2", "content":"error: Invalid number"}
      
      return result


def run():
  cherrypy.config.update({
      "environment": "production",
      "log.screen": True,
      "server.socket_port": 8003,
  })
  PIDFile(cherrypy.engine, 'microservice3.pid').subscribe()
  Daemonizer(cherrypy.engine).subscribe()
  cherrypy.quickstart(Root())


if __name__ == '__main__':
  run()
