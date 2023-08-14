from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "dbcentromedico"
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@app.route('/')
def index():   
    return render_template('admin_medico.html')

@app.route('/registrar_medico', methods=['POST'])
def registrar_medico():
    if request.method == 'POST':
        rfc = request.form['rfc']
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        correo = request.form['correo']
        password = request.form['password']
        rol = request.form['rol']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO admedicos (rfcmed, nombre, cedula, correo, contrasena, rol) VALUES (%s, %s, %s, %s, %s, %s)",
                    (rfc, nombre, cedula, correo, password, rol))
        mysql.connection.commit()
        cur.close()

        flash('Médico registrado exitosamente.', 'success')
        return redirect(url_for('index'))

@app.route('/eliminar_medico/<rfc>', methods=['GET', 'POST'])
def eliminar_medico(rfc):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM admedicos WHERE rfcmed = %s", (rfc,))
        mysql.connection.commit()
        cur.close()

        flash('Médico eliminado exitosamente.', 'success')
        return redirect(url_for('index'))

@app.route('/actualizar_medico/<rfc>', methods=['POST'])
def actualizar_medico(rfc):
    if request.method == 'POST':
        rfc = request.form['rfc']
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        correo = request.form['correo']
        password = request.form['password']
        rol = request.form['rol']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE admedicos SET nombre = %s, cedula = %s, correo = %s, contrasena = %s, rol = %s WHERE rfcmed = %s",
                    (nombre, cedula, correo, password, rol, rfc))
        mysql.connection.commit()
        cur.close()

        flash('Datos del médico actualizados exitosamente.', 'success')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
