#Se importa el modulo flask de la clase flask
from flask import Flask

#crea una instancia de la clase flask. el argumento __name__ le dice a flask que utilice el nombre del archivo actual main.py
app = Flask(__name__)

#este es un decorador que define una ruta corresponde a la pagina principal de la app
@app.route("/")
#cuando alguien visite la app (por ejemplo, http://localhost:5000/), la funcion hello() sera ejecutada
def hello():
    return "<h1>Hello World, Flask</h1>"

#solo se ejecuta si el archivo es ejecutado directamente arranca la aplicacion flask en modo depuracion (debug=True)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
