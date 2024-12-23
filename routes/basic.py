from flask import Blueprint, request, jsonify
from datetime import datetime
from models import ContactUs, db

BasicBP=Blueprint('BasicBP', __name__, template_folder='templates', static_folder='static')


@BasicBP.route('/contactus', methods=['POST'])
def createContactUsEntry():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request, no data provided"}), 400

        email = data.get('email')
        phone_number = data.get('phone_number')
        fullname = data.get('fullname')
        message = data.get('message')

        if not email or not phone_number or not fullname or not message:
            return jsonify({"error": "Missing required fields"}), 400

        newContactUsEntry = ContactUs(
            email=email,
            phone_number=phone_number,
            fullname=fullname,
            message=message,
        )

        db.session.add(newContactUsEntry)
        db.session.commit()

        return jsonify({
            "message": "ContactUs entry created successfully",
            "entry": {
                "id": newContactUsEntry.id,
                "email": email,
                "phone_number": phone_number,
                "fullname": fullname,
                "message": message,
                "created_at": newContactUsEntry.created_at
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
