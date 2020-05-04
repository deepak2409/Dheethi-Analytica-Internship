
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

#Configure db
db = yaml.load(open('db.yaml'))

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        name = details['name']
        id = details['id']
        email = details['email']
        phno = details['phone']
        feed = details['feed']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feed(name, id, email, phno, feed) VALUES (%s, %s, %s, %s, %s)", (name, id, email, phno,feed))
        mysql.connection.commit()
        cur.close()
        return redirect('/allfeedback')
    return render_template('index.html')
@app.route('/allfeedback', methods = ['GET'])
def feed():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("Select * from feed")
    if resultValue > 0:
        feedbacks = cur.fetchall()
        return render_template('feedbacks.html',feedbacks = feedbacks)
if __name__ == '__main__':
    app.run()
