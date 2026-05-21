from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# Create Flask app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

print("Database Location:", os.path.join(basedir, "database.db"))

# Enable CORS
CORS(app)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")

# Initialize database
db = SQLAlchemy(app)

# Create User Table
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    address = db.Column(db.String(200))


# Create database tables
with app.app_context():
    db.create_all()


# Register API
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    address = data.get("address")

    new_user = User(
        name=name,
        email=email,
        phone=phone,
        address=address
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    })


# GET ALL USERS
@app.route("/all-users", methods=["GET"])
def all_users():

    users = User.query.all()

    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        })

    return jsonify(user_list)


if __name__ == "__main__":
    app.run(debug=True)