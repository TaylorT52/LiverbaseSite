from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes
@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(email)
        print(password)
        #TODO: FIX
        user = db_session.query(User).where(User.email == email, User.password == password)
        print(user)

        if not user is None:
            print("success!")
        else:
            print("this is not a valid user")

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
