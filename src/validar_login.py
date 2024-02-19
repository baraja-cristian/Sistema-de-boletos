from db import mysql


def validar_login_user(user, password):
        user = user
        password = password
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT ID_estudiante FROM Usuario WHERE Usuario_cedula = %s AND Usuario_clave = %s',(user, password))
        respuesta = cursor.fetchall()
        cursor.close()
        return respuesta
        