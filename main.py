from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google import genai
import os
import re
import json
from datetime import datetime

# -----------------------
# INIT
# -----------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

app = Flask(__name__)


# -----------------------
# GEMINI AI PARSER
# -----------------------
def extract_info(user_text):
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
    Today's date is {today}.

    Extract structured information from this message.

    Return ONLY valid JSON:

    {{
      "date": "YYYY-MM-DD",
      "time": "HH:MM",
      "reason": "reason should describe the purpose of the appointment, not the booking request itself."
    }}

    Rules:
    - Convert relative dates (today, tomorrow, next Monday, etc.) using today's date.
    - time must be 24-hour format.
    - reason must be short (5-7 words max).

    Message:
    {user_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text

    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None

    except Exception as e:
        print("Parse error:", e)
        print("Raw response:", text)
        return None


# -----------------------
# HEALTH CHECK
# -----------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "AI Booking Backend is live"
    })


# -----------------------
# MAIN AI ENDPOINT (FOR MAKE.COM)
# -----------------------
@app.route("/book", methods=["POST"])
def book():

    try:
        data = request.get_json()

        message = data.get("message")
        name = data.get("name")
        email = data.get("email")

        if not message:
            return jsonify({
                "status": "error",
                "message": "Message is required"
            }), 400

        # AI extraction
        parsed = extract_info(message)

        if not parsed:
            return jsonify({
                "status": "error",
                "message": "Could not understand message"
            }), 400

        return jsonify({
            "status": "success",
            "message": "Appointment booked",
            "name": name,
            "email": email,
            "date": parsed.get("date","no date"),
            "time": parsed.get("time","no time"),
            "reason": parsed.get("reason","no reason")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/generate-unavailable-email", methods=["POST"])
def generate_unavailable_email():

    try:
        data = request.get_json()

        name = data.get("name")
        date = data.get("date")
        time = data.get("time")
        reason = data.get("reason")

        prompt = f"""
Write a complete professional email.

Customer Name: {name}
Requested Date: {date}
Requested Time: {time}
Appointment Reason: {reason}

Requirements:
- Politely inform the customer that the requested slot is unavailable.
- Thank them for their interest.
- Mention their requested date and time.
- Ask them to suggest another convenient time.
- Make the email ready to send.
- Do NOT include placeholders.
- Return ONLY the email body.
- Do not use '\\n'.
- return plain text only
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        email_text = response.text.replace("\n", " ").replace("\r", " ")

        return jsonify({
            "status": "success",
            "email_draft": email_text
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -----------------------
# RUN SERVER
# -----------------------
if __name__ == "__main__":
    app.run(debug=True,port=5005)