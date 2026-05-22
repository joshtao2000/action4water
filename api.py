import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
TO_EMAIL = "contact@action4water.org"

@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        organization = data.get("organization", "").strip()
        interest = data.get("interest", "").strip()
        message = data.get("message", "").strip()

        if not name or not email:
            return jsonify({"error": "Name and email are required."}), 400

        # Build email
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"Action4Water Partnership Inquiry from {name}"

        body = f"""
New partnership inquiry from Action4Water website:

Name: {name}
Email: {email}
Organization: {organization}
Interested in: {interest}
Message:
{message}
        """

        msg.attach(MIMEText(body, "plain"))

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
