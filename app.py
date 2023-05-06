from flask import *
from database import init_db, db_session
from models import *

UPLOAD_FOLDER = "uploaded-files"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# TODO: Change the secret key
app.secret_key = "Change Me"

@app.route("/savedslides", methods=["GET", "POST"])
def savedslides():
    return render_template("savedslides.html")

@app.route("/submitslides", methods=["GET", "POST"])
def submitslides():
    if request.method == "POST":
        f = request.files["file"].read()
        submission = Submission(request.form["donor_age"], request.form["percent_steatosis"], request.form["other_info"], f)
        db_session.add(submission)

        db_session.commit()
    
    return render_template("submitslides.html")

@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = db_session.query(User).where((User.email == email) & (User.password == password)).first()

        if not user == None:
            session["User"] = user.email
            return redirect(url_for("submitslides"))
        else:
            #TODO: instead of printing this, have appear on screen
            print("Incorrect user/password")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password-attempt2"]
        
        if password == password2:
            #TODO- is there a cleaner way to do this?? (add to list?)
            add_user = User(email = email, password = password)
            db_session.add(add_user)
            db_session.commit()
            print("success!")
            session["User"] = add_user.email
            return redirect(url_for("submitslides"))
        else:
            print("Doesn't match")
            return render_template("signup.html")
    else:
        return render_template("signup.html")

if __name__ == "__main__":
    init_db()
    app.run(port=5001)
