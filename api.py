import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
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

        msg = MIMEMultipart()
        msg["From"] = f"Action4Water <{GMAIL_USER}>"
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

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/report", methods=["POST"])
def send_report():
    try:
        data = request.get_json()

        user_email      = data.get("user_email", "").strip()
        recipient_email = data.get("recipient_email", "").strip()
        location        = data.get("location", "Unknown")
        datetime_str    = data.get("datetime", "Unknown")
        community       = data.get("community", "Unknown")
        water_body      = data.get("water_body", "Not specified")
        observation     = data.get("observation", "Not specified")
        severity        = data.get("severity", "Not specified")
        description     = data.get("description", "No description provided.")
        photo_base64    = data.get("photo_base64", None)

        if not user_email:
            return jsonify({"error": "User email is required."}), 400

        body = f"""
FIELD OBSERVATION REPORT — contact@action4water.org

Location:          {location}
Date/Time:         {datetime_str}
Nearest community: {community}
Water body:        {water_body}
Observation type:  {observation}
Severity:          {severity}

Description:
{description}

---
Sent via Northern Lakes Watch mobile app
        """

        def build_msg(to, subject, include_photo):
            m = MIMEMultipart()
            m["From"] = f"Northern Lakes Watch <{GMAIL_USER}>"
            m["Reply-To"] = "contact@action4water.org"
            m["To"] = to
            m["Subject"] = subject
            m.attach(MIMEText(body, "plain"))
            if include_photo and photo_base64:
                try:
                    img_data = base64.b64decode(photo_base64)
                    img = MIMEImage(img_data, name="field_photo.jpg")
                    img.add_header("Content-Disposition", "attachment", filename="field_photo.jpg")
                    m.attach(img)
                except Exception:
                    pass
            return m

        # Send report to recipient
        if recipient_email:
            msg_rec = build_msg(
                recipient_email,
                f"Water Quality Field Report — {water_body or community}",
                True
            )
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(GMAIL_USER, GMAIL_PASSWORD)
                server.sendmail(GMAIL_USER, recipient_email, msg_rec.as_string())

        # Send internal copy to contact@action4water.org
        msg_internal = build_msg(
            TO_EMAIL,
            f"[Field Report] {water_body or community} — {observation}",
            True
        )
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, TO_EMAIL, msg_internal.as_string())

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
