from app import app
from flask_mysqldb import MySQL

# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CrisBaraja10042'
app.config['MYSQL_DB'] = 'Systema_integracion'

# Inicializar la extensión MySQL
mysql = MySQL(app)
