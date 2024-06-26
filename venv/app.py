from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # Cargar variables del archivo .env

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')

# Define los detalles del servidor MySQL utilizando variables de entorno.
app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')

mysql = MySQL(app)

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Gestión de Empleados
@app.route('/empleados')
def empleados():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Empleados")
    if result_value > 0:
        empleados = cur.fetchall()
        return render_template('empleados.html', empleados=empleados)
    return render_template('empleados.html')

@app.route('/empleados/nuevo', methods=['GET', 'POST'])
def nuevo_empleado():
    if request.method == 'POST':
        empleado_details = request.form
        nombre = empleado_details['nombre']
        puesto = empleado_details['puesto']
        salario = empleado_details['salario']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Empleados(nombre, puesto, salario) VALUES(%s, %s, %s)", (nombre, puesto, salario))
        mysql.connection.commit()
        cur.close()
        flash('Empleado Agregado Satisfactoriamente', 'success')
        return redirect(url_for('empleados'))
    return render_template('nuevo_empleado.html')

@app.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Empleados WHERE id = %s", [id])
    empleado = cur.fetchone()

    if request.method == 'POST':
        empleado_details = request.form
        nombre = empleado_details['nombre']
        puesto = empleado_details['puesto']
        salario = empleado_details['salario']

        cur.execute("""
            UPDATE Empleados
            SET nombre = %s, puesto = %s, salario = %s
            WHERE id = %s
        """, (nombre, puesto, salario, id))
        mysql.connection.commit()
        cur.close()
        flash('Empleado Actualizado Satisfactoriamente', 'success')
        return redirect(url_for('empleados'))

    return render_template('editar_empleado.html', empleado=empleado)

@app.route('/empleados/eliminar/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    cur = mysql.connection.cursor()
    # Verificar si el empleado tiene asignaciones
    cur.execute("SELECT * FROM Asignaciones WHERE empleado_id = %s", [id])
    asignacion = cur.fetchone()
    if asignacion:
        flash('No se puede eliminar el empleado porque tiene asignaciones.', 'danger')
    else:
        cur.execute("DELETE FROM Empleados WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Empleado Eliminado Satisfactoriamente', 'success')
    cur.close()
    return redirect(url_for('empleados'))

# Gestión de Departamentos
@app.route('/departamentos')
def departamentos():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Departamentos")
    if result_value > 0:
        departamentos = cur.fetchall()
        return render_template('departamentos.html', departamentos=departamentos)
    return render_template('departamentos.html')

@app.route('/departamentos/nuevo', methods=['GET', 'POST'])
def nuevo_departamento():
    if request.method == 'POST':
        departamento_details = request.form
        nombre = departamento_details['nombre']
        ubicacion = departamento_details['ubicacion']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Departamentos(nombre, ubicacion) VALUES(%s, %s)", (nombre, ubicacion))
        mysql.connection.commit()
        cur.close()
        flash('Departamento Agregado Satisfactoriamente', 'success')
        return redirect(url_for('departamentos'))
    return render_template('nuevo_departamento.html')

@app.route('/departamentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_departamento(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Departamentos WHERE id = %s", [id])
    departamento = cur.fetchone()

    if request.method == 'POST':
        departamento_details = request.form
        nombre = departamento_details['nombre']
        ubicacion = departamento_details['ubicacion']

        cur.execute("""
            UPDATE Departamentos
            SET nombre = %s, ubicacion = %s
            WHERE id = %s
        """, (nombre, ubicacion, id))
        mysql.connection.commit()
        cur.close()
        flash('Departamento Actualizado Satisfactoriamente', 'success')
        return redirect(url_for('departamentos'))

    return render_template('editar_departamento.html', departamento=departamento)

@app.route('/departamentos/eliminar/<int:id>', methods=['POST'])
def eliminar_departamento(id):
    cur = mysql.connection.cursor()
    # Verificar si el departamento tiene asignaciones
    cur.execute("SELECT * FROM Asignaciones WHERE departamento_id = %s", [id])
    asignacion = cur.fetchone()
    if asignacion:
        flash('No se puede eliminar el departamento porque tiene asignaciones.', 'danger')
    else:
        cur.execute("DELETE FROM Departamentos WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Departamento Eliminado Satisfactoriamente', 'success')
    cur.close()
    return redirect(url_for('departamentos'))

# Gestión de Asignaciones
@app.route('/asignaciones')
def asignaciones():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Asignaciones")
    if result_value > 0:
        asignaciones = cur.fetchall()
        return render_template('asignaciones.html', asignaciones=asignaciones)
    return render_template('asignaciones.html')

@app.route('/asignaciones/nueva', methods=['GET', 'POST'])
def nueva_asignacion():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM Empleados")
    empleados = cur.fetchall()
    cur.execute("SELECT id, nombre FROM Departamentos")
    departamentos = cur.fetchall()

    if request.method == 'POST':
        asignacion_details = request.form
        empleado_id = asignacion_details['empleado_id']
        departamento_id = asignacion_details['departamento_id']
        fecha_asignacion = asignacion_details['fecha_asignacion']

        cur.execute("INSERT INTO Asignaciones(empleado_id, departamento_id, fecha_asignacion) VALUES(%s, %s, %s)", 
                    (empleado_id, departamento_id, fecha_asignacion))
        mysql.connection.commit()
        cur.close()
        flash('Asignación Agregada Satisfactoriamente', 'success')
        return redirect(url_for('asignaciones'))

    return render_template('nueva_asignacion.html', empleados=empleados, departamentos=departamentos)

@app.route('/asignaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_asignacion(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Asignaciones WHERE id = %s", [id])
    asignacion = cur.fetchone()

    cur.execute("SELECT id, nombre FROM Empleados")
    empleados = cur.fetchall()

    cur.execute("SELECT id, nombre FROM Departamentos")
    departamentos = cur.fetchall()

    if request.method == 'POST':
        asignacion_details = request.form
        empleado_id = asignacion_details['empleado_id']
        departamento_id = asignacion_details['departamento_id']
        fecha_asignacion = asignacion_details['fecha_asignacion']

        cur.execute("""
            UPDATE Asignaciones
            SET empleado_id = %s, departamento_id = %s, fecha_asignacion = %s
            WHERE id = %s
        """, (empleado_id, departamento_id, fecha_asignacion, id))
        mysql.connection.commit()
        cur.close()
        flash('Asignación Actualizada Satisfactoriamente', 'success')
        return redirect(url_for('asignaciones'))

    return render_template('editar_asignacion.html', asignacion=asignacion, empleados=empleados, departamentos=departamentos)

@app.route('/asignaciones/eliminar/<int:id>', methods=['POST'])
def eliminar_asignacion(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Asignaciones WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Asignación Eliminada Satisfactoriamente', 'success')
    return redirect(url_for('asignaciones'))

if __name__ == '__main__':
    app.run(debug=True)
