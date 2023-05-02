from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes
@app.route("/savedslides", methods=["GET", "POST"])
def savedslides():
    return render_template("savedslides.html")

@app.route("/submitslides", methods=["GET", "POST"])
def submitslides():
    return render_template("submitslides.html")

@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = db_session.query(User).where((User.email == email) & (User.password == password)).first()

        if not User == None:
            print("Success!")
            return redirect(url_for("submitslides"))
        else:
            print("Incorrect user/password")

    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password-attempt2"]
        
        if password == password2:
            add_user = User(email = email, password = password)
            db_session.add(add_user)
            db_session.commit()
            print("success!")
        else:
            print("Doesn't match")

    return render_template("signup.html")

if __name__ == "__main__":
    init_db()
    app.run(port=5001)
