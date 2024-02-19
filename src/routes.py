from flask import render_template, request, redirect, url_for, flash, session
from app import app
from validar_login import validar_login_user
from db import mysql
from datetime import datetime
import random
import string
@app.route('/')

def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST': # Si se envía el formulario
        user = request.form['user']
        password = request.form['password']
        
        if user == '' or password == '': # Si el usuario o contraseña están vacíos
            flash('Por favor ingrese usuario y contraseña')
            return redirect(url_for('index'))
        else:
            session_data = validar_login_user(user, password) # Llamar a la función que valida el usuario y contraseña
            if len(session_data) > 0: # Si el usuario y contraseña son correctos
                print(session_data)
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT Usuario_ID_rol FROM Usuario WHERE ID_estudiante = %s', (session_data))
                res_rol = cursor.fetchone()
                print (f"EL ROL ES {res_rol}")
                cursor.close()
                session['user'] = session_data # Guardar el usuario en la sesión
                print(session['user'])

                if res_rol[0] == '1' or res_rol[0] == '2':
                    #Rol de estudiante
                    flash('Usuario no permitido')
                    return redirect(url_for('index'))

                if res_rol[0] == '3' or res_rol[0] == '4':
                    #Rol de administrador y sub administrador
                    return redirect(url_for('home'))
            else:
                flash('El usuaro no existe o la contraseña es incorrecta')
                return redirect(url_for('index'))
            
@app.route('/home')
def home():
    if 'user' in session: # Si el usuario está en la sesión
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Usuario WHERE ID_estudiante = %s', (session['user']))
        res = cursor.fetchone()
        data_user_log = (res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8])
        cursor.execute("""
            SELECT Rol_usuario.Tipo_rol, Rol_usuario.ID_rol_usuario
            FROM Usuario 
            INNER JOIN Rol_usuario ON Rol_usuario.ID_rol_usuario = Usuario.Usuario_ID_rol 
            WHERE Usuario.ID_estudiante = %s
        """, (session['user'],))

        rol_user = cursor.fetchone()
        
        session['data_user_log'] = data_user_log
        session['rol_user'] = rol_user
        print(session['rol_user'])
        cursor.close()
        
        return render_template('home.html', data_user_log = data_user_log, rol_user = rol_user)
    else:
        return redirect(url_for('index'))
    
    
@app.route('/roles')
def roles():
    if 'user' in session:
        if session['rol_user'][1] == '3':
            data_user_log = session.get('data_user_log')
            rol_user = session.get('rol_user')

            cursor = mysql.connection.cursor()
            cursor.execute("""
                           SELECT Usuario.ID_estudiante, Usuario.Usuario_cedula, Usuario.Usuario_nombre1, Usuario.Usuario_nombre2,  Usuario.Usuario_apellido1, Usuario_apellido2, Rol_usuario.Tipo_rol
                           FROM Usuario 
                           INNER JOIN Rol_usuario ON Rol_usuario.ID_rol_usuario = Usuario.Usuario_ID_rol""")

            res_datos_usuarios = cursor.fetchall()
            cursor.close()
            return render_template('roles.html', data_user_log=data_user_log, rol_user=rol_user, res_datos_usuarios=res_datos_usuarios)
        else:
            flash('No estas autorizado para ver esta página')
            return redirect(url_for('home'))
    else:
       return redirect(url_for('index'))
   
@app.route('/edit/<string:id>')
def edit(id):
    if 'user' in session and session['rol_user'][1] == '3':
        data_user_log = session.get('data_user_log')
        rol_user = session.get('rol_user')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Usuario WHERE ID_estudiante = %s', (id))
        data_edit_user = cursor.fetchall()
        return render_template('edit_rol.html', data_edit_user = data_edit_user[0], data_user_log=data_user_log, rol_user=rol_user)
    else:
        return redirect(url_for('index'))
    
@app.route('/actualizar/<string:id>', methods=['POST'])
def actualizar(id):
    if 'user' in session:
        cedula = request.form['cedula']
        nombre1 = request.form['nombre1']
        nombre2 = request.form['nombre2']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        email = request.form['email']
        password = request.form['password']
        rol= request.form['rol']
        print(cedula, nombre1, nombre2, apellido1, apellido2, email, password, rol)
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
                    UPDATE Usuario
                    SET Usuario_cedula = %s, Usuario_nombre1 = %s, Usuario_nombre2 = %s, Usuario_apellido1 = %s, Usuario_apellido2 = %s, Usuario_correo = %s, Usuario_clave = %s, Usuario_ID_rol = %s
                    WHERE ID_estudiante = %s
                    """, (cedula, nombre1, nombre2, apellido1, apellido2, email, password, rol, id))
        mysql.connection.commit()
        cursor.close()
        flash('Usuario actualizado')
        return redirect(url_for('roles'))
    else:
        return redirect(url_for('index'))

@app.route('/buscarUser', methods=['POST'])
def buscarUser():
    if 'user' in session:
        if request.method == 'POST':
            
            buscar = request.form['buscar']
            cursor = mysql.connection.cursor()
            
            cursor.execute('SELECT * FROM Usuario WHERE Usuario_cedula = %s', (buscar,))
            res = cursor.fetchone()
            cursor.close()


            if res is not None and len(res) > 0:
                return redirect(url_for('edit', id=res[0]))
            else:
                flash('El usuario no existe')
                return redirect(url_for('roles'))
    else:
        return redirect(url_for('index'))

@app.route('/compra')
def compra():
    if 'user' in session:
        data_user_log = session.get('data_user_log')
        rol_user = session.get('rol_user')

        cursor_factura = mysql.connection.cursor()

        cursor_factura.execute("""
            SELECT 
                Factura.ID_factura, 
                Compra_boleto.Fecha_boleto, 
                Boleto_tipo.Tipo_boleto_tipo,
                CONCAT(Usuario.Usuario_nombre1, ' ', Usuario.Usuario_apellido1) AS Nombre_cliente
            FROM 
                Factura 
                INNER JOIN Compra_boleto ON Factura.Compra_ID_boleto = Compra_boleto.ID_compra_boleto
                INNER JOIN Usuario ON Compra_boleto.Usuario_ID_cliente = Usuario.ID_estudiante
                INNER JOIN Boleto_tipo ON Factura.Boleto_ID_tipo = Boleto_tipo.ID_boleto_tipo
                WHERE Compra_boleto.Usuario_ID_vendedor = %s
        """, (data_user_log[0],))

        res_factura = cursor_factura.fetchall()

        cursor_factura.close()

        return render_template('compra.html', data_user_log=data_user_log, rol_user=rol_user, res_factura=res_factura)
    else:
        return redirect(url_for('index'))

@app.route('/buscar_datos_compra', methods=['POST'])
def buscar_datos_compra():
    if 'user' in session:
        data_user_log = session.get('data_user_log')
        rol_user = session.get('rol_user')
        fecha_actual = datetime.now()
        fecha = fecha_actual.date()
        if request.method == 'POST':
            buscar = request.form['buscar']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM Usuario WHERE Usuario_cedula = %s', (buscar,))
            res = cursor.fetchone()
            session['id_usuario_compra'] = res[0]
            cursor.close()

            cursor2 = mysql.connection.cursor()
            cursor2.execute('SELECT * FROM Metodo_pago ')
            metodo_pago = cursor2.fetchall()
            cursor2.close()


            cursor3 = mysql.connection.cursor()
            cursor3.execute('SELECT * FROM Boleto_tipo ')
            tipo_entrada = cursor3.fetchall()
            cursor3.close()

            if res is not None and len(res) > 0:
                return render_template('vender_boleto.html', data_user_log=data_user_log, rol_user=rol_user, res=res, fecha=fecha, metodo_pago=metodo_pago, tipo_entrada=tipo_entrada)
            else:
                flash('El usuario no existe')
                return redirect(url_for('roles'))
    else:
        return redirect(url_for('index'))


@app.route('/realizar_compra', methods=['POST'])
def realizar_compra():
    if 'user' in session:
        if request.method == 'POST':
            fecha_de_compra = request.form['fecha_de_compra']
            datos_cliente = session.get('id_usuario_compra')
            datos_vendedor = session.get('data_user_log')[0]
            metodo_pago = request.form['metodo_pago']
            tipo_entrada = request.form['tipo_entrada']

            # Generar un número aleatorio y letras al azar
            numero_aleatorio = str(random.randint(1, 9999))
            letras_aleatorias = ''.join(random.choices(string.ascii_letters, k=8))
            # Concatenar el número y las letras
            id_generado = numero_aleatorio + "-" + letras_aleatorias

            cursor_comprar_boleto = mysql.connection.cursor()
            cursor_comprar_boleto.execute('INSERT INTO Compra_boleto(ID_compra_boleto, Fecha_boleto, Usuario_ID_cliente, Usuario_ID_vendedor, Metodo_ID_pago) VALUES (%s, %s, %s, %s, %s)', (id_generado, fecha_de_compra, datos_cliente, datos_vendedor, metodo_pago))
            mysql.connection.commit()
            cursor_comprar_boleto.close()

            # Concatenar el número y las letras
            # Generar un número aleatorio y letras al azar
            letras_aleatorias_fac = ''.join(random.choices(string.ascii_letters, k=8))
            numero_aleatorio_fac = str(random.randint(1, 9999))
            id_generado_factura = letras_aleatorias_fac + "-" +  numero_aleatorio_fac

            cursor_factura = mysql.connection.cursor()
            cursor_factura.execute('INSERT INTO Factura(ID_factura, Compra_ID_boleto, Boleto_ID_tipo) VALUES (%s, %s, %s)', (id_generado_factura, id_generado, tipo_entrada))
            mysql.connection.commit()
            cursor_factura.close()

            return redirect(url_for('compra'))

    else:
        return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run( host='192.168.0.112', port=5000, debug = True)