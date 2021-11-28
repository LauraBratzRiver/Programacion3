from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
import json
import crud_alumnos
import crud_docentes
import escalafon

crud_alumnos = crud_alumnos.crud_alumnos()
crud_docentes = crud_docentes.crud_docentes()
escalafon = escalafon.escalafon()
class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path=="/consulta-alumno":
            resp = crud_alumnos.consultar()
            resp = json.dumps(dict(data=resp))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp.encode("utf-8"))
        
        elif self.path=="/consulta-docente":
            resp = crud_docentes.consultar()
            resp = json.dumps(dict(data=resp))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp.encode("utf-8"))
        
        elif self.path=="/consulta-escalafon":
            resp = escalafon.consultar()
            resp = json.dumps(dict(data=resp))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp.encode("utf-8"))
        
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        longitud_contenido = int(self.headers['Content-Length'])
        contenido = self.rfile.read(longitud_contenido)
        contenido = contenido.decode("utf-8")
        contenido = parse.unquote(contenido)
        contenido = json.loads(contenido)
        if self.path=="/alumno":
            resp = crud_alumnos.administrar_alumno(contenido)
        elif self.path=="/docente":
            resp = crud_docentes.administrar_docentes(contenido)
        resp = json.dumps(dict(resp=resp))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(resp.encode("utf-8"))

print("Servidor iniciado")
server = HTTPServer(("localhost", 3000), servidorBasico)
server.serve_forever()