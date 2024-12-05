"""
CRUD FLASK PYTHON + MYSQL
Desarrollado por: Cristian Redondo
"""

#Importando  flask y algunos paquetes
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import date
from datetime import datetime

from bd import *  #Importando conexion BD
from controlador_usuarios import *  #Importando controlador_usuarios
from routes import * #Vistas

import re
from werkzeug.security import generate_password_hash, check_password_hash

# Importamos el controlador
import controlador_juegos



# Ruta: /ruta principal
@app.route("/")
@app.route("/inicio")
def index():
    return redirect(url_for('loginUser'))

#Ruta: juegos
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("public/dashboard/juegos/juegos.html", juegos=juegos)

# Ruta: agregar_juego
@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("public/dashboard/juegos/agregar_juego.html")

# Ruta: guardar_juego
@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    # Recibe los datos del formulario
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    # Guarda los datos en la base de datos ingresando a la función inserta_juego
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/juegos")

# Ruta: eliminar_juego
@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect("/juegos")

# Ruta: formulario_editar_juego
@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    # Obtener el juego por ID
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("public/dashboard/juegos/editar_juego.html", juego=juego)

# Ruta: actualizar_juego
@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

# Ruta: detalles_juego
@app.route("/detalles_juego/<int:id>")
def detalles(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("public/dashboard/juegos/detalles_juego.html", juego=juego)

@app.route('/dashboard', methods=['GET', 'POST'])
def loginUser():
    conexion_MySQLdb = connectionBD()
    if 'conectado' in session:
        return render_template('public/dashboard/home.html', dataLogin = dataLoginSesion())
    else:
        msg = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email      = str(request.form['email'])
            password   = str(request.form['password'])
            
            # Comprobando si existe una cuenta
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", [email])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['password'],password):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas 
                    session['conectado']        = True
                    session['id']               = account['id']
                    session['tipo_user']        = account['tipo_user']
                    session['nombre']           = account['nombre']
                    session['apellido']         = account['apellido']
                    session['email']            = account['email']
                    session['sexo']             = account['sexo']
                    session['pais']             = account['pais']
                    session['create_at']        = account['create_at']
                    session['te_gustan_los_videojuegos']     = account['te_gustan_los_videojuegos']

                    msg = "Ha iniciado sesión correctamente."
                    return render_template('public/dashboard/home.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion())                    
                else:
                    msg = 'Datos incorrectos, por favor verfique!'
                    return render_template('public/modulo_login/index.html', msjAlert = msg, typeAlert=0)
            else:
                return render_template('public/modulo_login/index.html', msjAlert = msg, typeAlert=0)
    return render_template('public/modulo_login/index.html', msjAlert = 'Debe iniciar sesión.', typeAlert=0, dataPaises = listaPaises())

#Registrando una cuenta de Usuario
@app.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    msg = ''
    conexion_MySQLdb = connectionBD()
    if request.method == 'POST':
        tipo_user                   =1
        nombre                      = request.form['nombre']
        apellido                    = request.form['apellido']
        email                       = request.form['email']
        password                    = request.form['password']
        repite_password             = request.form['repite_password']
        sexo                        = request.form['sexo']
        te_gustan_los_videojuegos    = request.form['te_gustan_los_videojuegos']
        pais                        = request.form['pais']
        create_at                   = date.today()
        #current_time = datetime.datetime.now()

        # Comprobando si ya existe la cuenta de Usuario con respecto al email
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        account = cursor.fetchone()
        cursor.close() #cerrrando conexion SQL

        if account:
            msg = 'Ya existe el Email!'
        elif password != repite_password:
            msg = 'Disculpa, las clave no coinciden!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Disculpa, formato de Email incorrecto!'
        elif not email or not password or not password or not repite_password:
            msg = 'El formulario no debe estar vacio!'
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            password_encriptada = generate_password_hash(password, method='scrypt')
            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute('INSERT INTO usuarios (tipo_user, nombre, apellido, email, password, sexo, pais, create_at, te_gustan_los_videojuegos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (tipo_user, nombre, apellido, email, password_encriptada, sexo, pais, create_at, te_gustan_los_videojuegos))
            conexion_MySQLdb.commit()
            cursor.close()
            msg = 'Cuenta creada correctamente!'

        return render_template('public/modulo_login/index.html', msjAlert = msg, typeAlert=1, dataPaises = listaPaises())
    return render_template('public/layout.html', dataLogin = dataLoginSesion(), msjAlert = msg, typeAlert=0)


@app.route('/actualizar-mi-perfil/<id>', methods=['POST'])
def actualizarMiPerfil(id):
    if 'conectado' in session:
        msg = ''
        if request.method == 'POST':
            nombre        = request.form['nombre']
            apellido      = request.form['apellido']
            email         = request.form['email']
            sexo          = request.form['sexo']
            pais          = request.form['pais']

            if(request.form['password']):
                password         = request.form['password'] 
                repite_password  = request.form['repite_password'] 
                
                if password != repite_password:
                    msg ='Las claves no coinciden'
                    return render_template('public/dashboard/home.html', msjAlert = msg, typeAlert=0, dataLogin = dataLoginSesion())
                else:
                    nueva_password = generate_password_hash(password, method='sha256')
                    conexion_MySQLdb = connectionBD()
                    cur = conexion_MySQLdb.cursor()
                    cur.execute("""
                        UPDATE usuarios 
                        SET 
                            nombre = %s, 
                            apellido = %s, 
                            email = %s, 
                            sexo = %s, 
                            pais = %s, 
                            password = %s
                        WHERE id = %s""", (nombre, apellido, email, sexo, pais, nueva_password, id))
                    conexion_MySQLdb.commit()
                    cur.close() #Cerrando conexion SQL
                    conexion_MySQLdb.close() #cerrando conexion de la BD
                    msg = 'Perfil actualizado correctamente'
                    return render_template('public/dashboard/home.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion())
            else:
                msg = 'Perfil actualizado con exito'
                conexion_MySQLdb = connectionBD()
                cur = conexion_MySQLdb.cursor()
                cur.execute("""
                    UPDATE usuarios 
                    SET 
                        nombre = %s, 
                        apellido = %s, 
                        email = %s, 
                        sexo = %s, 
                        pais = %s
                    WHERE id = %s""", (nombre, apellido, email, sexo, pais, id))
                conexion_MySQLdb.commit()
                cur.close()
                return render_template('public/dashboard/home.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion())
        return render_template('public/dashboard/home.html', dataLogin = dataLoginSesion())

# Iniciar el servidor para ejecutar la aplicación flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)