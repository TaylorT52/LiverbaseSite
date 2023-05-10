from flask import *
from database import init_db, db_session
from models import *
import base64
import process

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

@app.route("/logout")
def logout():
    session.pop("Username", None)
    return redirect(url_for("signin"))

@app.route("/savedslides/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    submissions = db_session.query(User).where(User.email == session["User"]).first().submissions
    del_sub = submissions[entry_id-1]
    db_session.delete(del_sub)
    db_session.commit()
    return "Success", 200

@app.route("/savedslides", methods=["GET", "POST"])
def savedslides():
    saved_slides = db_session.query(User).where(User.email == session["User"]).first().submissions
    show = []

    for slide in saved_slides:
        result = slide.result[0]
        temp = {
            "percent_steatosis": slide.percent_steatosis,
            "donor_age": slide.donor_age,
            "other_info": slide.other_info,
            "file": base64.b64encode(slide.file),
            "ret_steatosis": round(result.percent_steatosis,2),
            "image": base64.b64encode(result.mask)
        }
        show.append(temp)
    return render_template("savedslides.html", saved_slides = show)

@app.route("/submitslides", methods=["GET", "POST"])
def submitslides():
    if request.method == "POST":
        f = request.files["file"]
        f = f.read()
        if(f):
            submission = Submission(session["User"], request.form["donor_age"], request.form["percent_steatosis"], request.form["other_info"], f)
            db_session.add(submission)
            db_session.commit()
            steatosis, img = model.tile_slide(f)
            if not steatosis == -1:
                results = Result(submission.submission_id, steatosis, img)
                db_session.add(results)
                db_session.commit()
                session["submission_id"] = submission.submission_id
                return redirect(url_for("results"))
            else: 
                print(submission)
                db_session.remove(submission)
                db_session.commit()
                return render_template("submitslides.html")
        else: 
            flash("Missing image upload!", "error")
    return render_template("submitslides.html")

@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        session["User"] = None
        email = request.form["email"]
        password = request.form["password"]
        user = db_session.query(User).where((User.email == email) & (User.password == password)).first()

        if not user == None:
            session["User"] = user.email
            return redirect(url_for("submitslides"))
        else:
            flash("Incorrect username/password", "error")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password-attempt2"]
        
        user = db_session.query(User).where((User.email == email) & (User.password == password)).first()

        if password == password2 and user is None:
            add_user = User(email = email, password = password)
            db_session.add(add_user)
            db_session.commit()
            print("success!")
            session["User"] = add_user.email
            return redirect(url_for("submitslides"))
        elif not user is None:
            flash("This user already exists", "error")
            return render_template("signup.html")
        else:
            flash("Passwords do not match!", "error")
            return render_template("signup.html")
    else:
        return render_template("signup.html")

@app.route("/results", methods=["GET"])
def results():
    sub = db_session.query(Submission).where(Submission.submission_id == session["submission_id"]).first()
    res = base64.b64encode(sub.result[0].mask)
    percent_steatosis = round(sub.result[0].percent_steatosis, 2)
    return render_template("results.html", results=res, submission=base64.b64encode(sub.file), percent_steatosis=percent_steatosis)

if __name__ == "__main__":
    init_db()
    model = process.Process
    app.run(port="5001", debug=True)
