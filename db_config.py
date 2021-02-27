from app import app
from flaskext.mysql import MySQL
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Tech2486'
app.config['MYSQL_DATABASE_DB'] = 'moviedb'
app.config['MYSQL_DATABASE_HOST'] = 'firstdb.chusjycs1js9.us-east-2.rds.amazonaws.com'
mysql.init_app(app)
