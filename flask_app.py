
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin,logout_user,login_required,current_user
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="dheetiInterns",
    password="Dsqlpass",
    hostname="dheetiInterns.mysql.pythonanywhere-services.com",
    databasename="dheetiInterns$comments",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = "something only you know"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

all_users = {
    "admin": User("admin", generate_password_hash("secret")),
    "bob": User("bob", generate_password_hash("less-secret")),
    "caroline": User("caroline", generate_password_hash("completely-secret")),
}
@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

class Feed(db.Model):

    __tablename__ = "feed"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    idno = db.Column(db.String(30))
    email = db.Column(db.String(30))
    phno = db.Column(db.String(30))
    grade = db.Column(db.String(30))
    feed = db.Column(db.String(4096))






@app.route("/", methods=["GET", "POST"])

def index():
    if request.method == "GET":
        return render_template("main_page.html")
    if request.method == "POST":
        name = request.form['name']
        idno = request.form['idno']
        email = request.form['email']
        phno = request.form['phone']
        grade = request.form['grade']
        feeds = request.form['feed']

        feed = Feed(name= name, idno = idno ,email = email,phno = phno, grade = grade,feed = feeds)
        db.session.add(feed)
        db.session.commit()
        return redirect('/allfeedback')

@app.route('/allfeedback', methods = ['GET'])
def feeds():
    if  current_user.is_authenticated:
        # return render_template('feedbacks.html', comments=Comment.query.all())
        return render_template('feedbacks.html', query = Feed.query.all())
    if not current_user.is_authenticated:
        return render_template('feedbacks.html')
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    username = request.form["username"]
    if username not in all_users:
        return render_template("login_page.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('feeds'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))