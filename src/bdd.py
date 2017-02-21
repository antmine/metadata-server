import json

from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

with open('config.json', 'r') as file:
    configMySql = json.load(file)["mysql"]

    app.config['MYSQL_DATABASE_USER'] = configMySql["user"]
    app.config['MYSQL_DATABASE_PASSWORD'] = configMySql["password"]
    app.config['MYSQL_DATABASE_HOST'] = configMySql["url"]
    app.config['MYSQL_DATABASE_DB'] = configMySql["database"]
    mysql.init_app(app)

    cursor = mysql.connect().cursor()

    ####### Exemple SQL #######

    sql = "SELECT * from WEBSITE;"
    cursor.execute(sql)
    data = cursor.fetchall()

    for website in data:
        print(website)
