from flask import *
from database import init_db, db_session
from models import *
import base64
import process

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

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

    #need this so that img is base64 encoded
    for slide in saved_slides:
        temp = {
            "percent_steatosis": slide.percent_steatosis,
            "donor_age": slide.donor_age,
            "other_info": slide.other_info,
            "file": base64.b64encode(slide.file)
        }
        show.append(temp)

    return render_template("savedslides.html", saved_slides = show)

@app.route("/submitslides", methods=["GET", "POST"])
def submitslides():
    if request.method == "POST":
        f = request.files["file"]
        f = f.read()
        #TODO: Clean up
        submission = Submission(session["User"], request.form["donor_age"], request.form["percent_steatosis"], request.form["other_info"], f)
        db_session.add(submission)
        db_session.commit()
        steatosis, img = model.tile_slide(f)
        results = Result(submission.submission_id, steatosis, img)
        db_session.add(results)
        db_session.commit()
        flash("Success!")
        session["submission_id"] = submission.submission_id
        return redirect(url_for("results"))
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
            #TODO: instead of printing this, have appear on screen -- Can use flash
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

@app.route("/results", methods=["GET"])
def results():
    res = db_session.query(Result).where(Result.submission_id == session["submission_id"]).first()
    return render_template("results.html", results=res)

if __name__ == "__main__":
    init_db()
    model = process.Process
    app.run(port=5001, debug=True)
