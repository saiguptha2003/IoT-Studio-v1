import json
from sqlite3 import IntegrityError, OperationalError
from flask import Flask, Blueprint, jsonify, request, Response,session
from werkzeug.security import check_password_hash
from utils import hashPassword,checkPassword
from models import User,db
from utils import getUniqueID
from utils import create_token
from services import createDocumentForUser
authBP = Blueprint('authBP', __name__, template_folder='templates', static_folder='static')

@authBP.route('/signup',methods=['POST'])
def signup():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    if not email or not username or not password:
        return jsonify({"error": "Email, Username, and Password are required"}), 400

    existingEmail = User.query.filter_by(email=email).first()
    if existingEmail:
        return jsonify({"error": "Email is already registered"}), 400

    existingUsername = User.query.filter_by(user_name=username).first()
    if existingUsername:
        return jsonify({"error": "Username is already registered"}), 400

    hashedPassword = hashPassword(password)
    uniqueID = getUniqueID()

    try:
        newUser = User(email=email, user_name=username, password_hash=hashedPassword, uniqueID=uniqueID)
        db.session.add(newUser)
        db.session.commit()
        couchDBResponse=json.loads(createDocumentForUser(newUser.uniqueID,newUser.user_name,newUser.email))
        return jsonify({"success": True, "message": "User signed up successfully! document", "status_code":couchDBResponse['status_code']}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "IntegrityError",
            "message": "A user with the same email or unique ID already exists."
        }), 400
    except OperationalError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "OperationalError",
            "message": "Database operation failed. Please check the database connection."
        }), 500


@authBP.route('/signin',methods=['POST'])
def signin():
    data = request.get_json()
    username_or_email = data.get("username_or_email") 
    password = data.get("password")
    if not username_or_email or not password:
        return jsonify({"message": "Username/Email and password are required"}), 400
    user = User.query.filter(
        (User.user_name == username_or_email) | (User.email == username_or_email)
    ).first()
    if user and checkPassword(password,user.password_hash):
        session["user_id"] = user.uniqueID
        session["username"] = user.user_name
        token = create_token(user.user_name, additional_claims={"userid": user.uniqueID,"email":user.email})
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user_id": user.uniqueID,
            "email":user.email
        }), 200
    else:
        return jsonify({"message": "Invalid username/email or password"}), 401
    
@authBP.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "email": user.email,
            "username": user.user_name,
            "unique_id": user.uniqueID,
        }
        for user in users
    ]
    
    return jsonify(user_list), 200
