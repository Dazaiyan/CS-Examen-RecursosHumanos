from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from os import getenv
from dotenv import load_dotenv
import random

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Se establece la clave secreta directamente

# Configuración de la base de datos
app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'recursosdb'

mysql = MySQL(app)

# Clase Nodo para consenso
class Nodo:
    def __init__(self, id, salario):
        self.id = id
        self.salario = salario

    def __repr__(self):
        return f"Nodo-{self.id}: {self.salario}"

# Función de consenso: mayoría simple
def consenso_por_mayoria(nodos):
    propuestas = [nodo.salario for nodo in nodos]
    conteo = {salario: propuestas.count(salario) for salario in set(propuestas)}
    return max(conteo, key=conteo.get)

# Página principal: lista de empleados
@app.route('/')
def empleados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, puesto, salario FROM Empleados")
    empleados = cur.fetchall()
    cur.close()
    return render_template('empleados.html', empleados=empleados)

# Crear un nuevo empleado
@app.route('/empleados/nuevo', methods=['GET', 'POST'])
def nuevo_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        puesto = request.form['puesto']

        # Simulación de nodos votando por un salario
        nodos = [Nodo(id=i, salario=random.choice([1000, 2000, 3000])) for i in range(5)]
        salario_consenso = consenso_por_mayoria(nodos)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Empleados (nombre, puesto, salario) VALUES (%s, %s, %s)", 
                    (nombre, puesto, salario_consenso))
        mysql.connection.commit()
        cur.close()
        flash(f'Empleado creado con salario consensuado: {salario_consenso}', 'success')
        return redirect(url_for('empleados'))
    return render_template('nuevo_empleado.html')

# Editar empleado
@app.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Empleados WHERE id = %s", [id])
    empleado = cur.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        puesto = request.form['puesto']
        salario = request.form['salario']

        cur.execute("UPDATE Empleados SET nombre=%s, puesto=%s, salario=%s WHERE id=%s", 
                    (nombre, puesto, salario, id))
        mysql.connection.commit()
        cur.close()
        flash('Empleado actualizado satisfactoriamente', 'success')
        return redirect(url_for('empleados'))

    cur.close()
    return render_template('editar_empleado.html', empleado=empleado)

# Eliminar empleado
@app.route('/empleados/eliminar/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Empleados WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Empleado eliminado satisfactoriamente', 'success')
    return redirect(url_for('empleados'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
