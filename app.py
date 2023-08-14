from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL



# inicializamos el servidor flask
app= Flask(__name__,static_folder='static',template_folder='templates')

#configuraciones para la conexion a la BD
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbcentromedico"

app.secret_key='mysecretkey'

mysql=MySQL(app)



#declaramos una ruta

#ruta index o principal http://localhost:5000
#la ruta se compone de nombre y la funcion
@app.route('/')
def index():
    return render_template('login.html')



@app.route('/iniciar', methods=['POST'])
def iniciar():

        nombre= request.form['txtrfc']
        contrasena= request.form['txtpassword']
        CS = mysql.connection.cursor()
        CS.execute('select * from admedicos where rfcmed=(%s) and contrasena=(%s)', (nombre,contrasena))
       
        if (CS.rowcount == 1):
            
            flash('Acceso correcto')
            return render_template('registrarPac.html')
        else:
            flash('Usuario o contraseña incorrecta')
            return render_template('login.html')


@app.route('/guardarp',methods=['POST'])
def guardar():
    if request.method == 'POST':
        nombre= request.form['txtpac']
        fecha= request.form['fecha']
        enfermedades= request.form['enfermedades']
        alergias= request.form['alergias']
        antecedentes= request.form['antecedentes']
        CS = mysql.connection.cursor()
        CS.execute('insert into adpac (nombreP,fecha_nac,encronias,alergias,antecedentes) values(%s,%s,%s,%s,%s)',(nombre,fecha,enfermedades,alergias,antecedentes))
        mysql.connection.commit()

    flash('Usuario guardado')
    return render_template('registrarPac.html')


@app.route('/edi')
def edi():
    return render_template('editarPac.html')

@app.route('/editarp',methods=['POST'])
def editarp():
    if request.method == 'POST':
        nombreEdit= request.form['txtpacEdit']
        nombre= request.form['txtpac']
        fecha= request.form['fecha']
        enfermedades= request.form['enfermedades']
        alergias= request.form['alergias']
        antecedentes= request.form['antecedentes']
        CS= mysql.connection.cursor()
        CS.execute("UPDATE adpac SET nombreP=%s, fecha_nac=%s, encronias=%s, alergias=%s, antecedentes=%s WHERE nombreP=%s", (nombre,fecha,enfermedades,alergias,antecedentes,nombreEdit))
        CS.commit()

    return render_template('login.html')

#ejecucion 
if __name__== '__main__':
    app.run(port= 5000, debug=True)