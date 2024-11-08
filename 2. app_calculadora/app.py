#Importamos la clases y métodos con las que trabajamos
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=["GET", "POST"])

def aritmetica():
    if request.method == "POST":
        #Valores que recibo del form n1,n2 son pasados
        num1 = float(request.form.get('n1'))
        num2 = float(request.form.get('n2'))

        #Realizamos operaciones aritmeticas 
        suma = num1 + num2
        resta = num1 - num2
        multiplicacion = num1 * num2
        division = num1 / num2

        return render_template('index.html', total_suma = suma, 
                                            total_resta = resta,
                                            total_multiplicacion = multiplicacion,
                                            total_division = division)

    return render_template('index.html')

#-------------------------------------------------------------------------------------------------

@app.route('/divisa', methods=['GET', 'POST'])

def divisa():

    DOLAR = 4400

    if request.method == "POST":
        #valor que recibo de valor, son convertidos a decimales
        valor = float(request.form.get('valor'))

        #realizamos la conversion
        conversion = valor * DOLAR
        return render_template('divisa.html', resultado = conversion, dolares = valor)
    
    return render_template('divisa.html')
#-------------------------------------------------------------------------------------------------

@app.route("/fechas")
def fechas():
    return render_template("fechas.html")

@app.route("/longitudes")
def longitudes():
    return render_template("longitudes.html")

if __name__ == "__main__":
    app.run(debug=True)