from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'myuser'
app.config['MYSQL_PASSWORD'] = 'mypass'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        name = details['name']
        mail = details['mail']
        comment = details['comment']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bookinfo(name, mail, comment) VALUES (%s, %s, %s)", (name, mail, comment))
        mysql.connection.commit()
        cur.close()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')