from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'vso987q0948htg0834hfp9bwqsnod8f7qg03rw87fgpw94t8gh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.errorhandler(500)
def internal_server_error(error):
    return "Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.", 500

@app.route('/')
def home():
    income = request.args.get('income')
    expense = request.args.get('expense')
    percent = 0
    if income and expense:
        try:
            income = float(income)
            expense = float(expense)
            if income > 0:
                percent = (expense / income) * 100
        except ValueError:
            pass  # Handle the error if needed

    return render_template('home.html', percent=percent)

@app.route('/process_data', methods=['POST'])
def process_data():
    income = request.form.get('income')
    expense = request.form.get('expense')
    return redirect(url_for('home', income=income, expense=expense))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/contact')
def contact():
    contacts = [{"name": 'Ansar', 'number': '8 776 119 55-11'}]
    return render_template('contact.html', contacts=contacts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        print(f"Login Attempt - Username: {uname}, Password: {passw}")

        if not uname or not passw:
            print("Form Error: All fields are required.")
            return render_template("log.html", error="All fields are required.")

        user = User.query.filter_by(username=uname).first()

        if user and user.password == passw:
            session['user_id'] = user.id
            print("Login successful.")
            return redirect(url_for("home"))
        else:
            print("Invalid username or password.")
            return render_template("log.html", error="Invalid username or password.")

    return render_template("log.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        # Debugging: Print the form data
        print(f"Username: {uname}, Email: {mail}, Password: {passw}")

        if not uname or not mail or not passw:
            return render_template("reg.html", error="All fields are required.")

        new_user = User(username=uname, email=mail, password=passw)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            print("User registered successfully.")
            return redirect(url_for("login"))
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {e}")
            return render_template("reg.html", error="Username or email already exists.")
        except Exception as e:
            db.session.rollback()
            print(f"Other Exception: {e}")
            return render_template("reg.html", error="An error occurred during registration. Please try again.")
    
    return render_template("reg.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
