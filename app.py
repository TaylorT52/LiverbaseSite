from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes

if __name__ == "__main__":
    init_db()
    app.run(port=5001)
