from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv("key.env")

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    prompt = f"""
    Based on the following project details, generate a concise summary of the project scope:

    Project Title: {data.get("what_is_the_title_or_brief_name_of_your_project")}
    Project Description: {data.get("what_is_the_project_about")}
    Main Goals/Objectives: {data.get("what_are_the_main_goals_or_objectives")}
    Stakeholders: {data.get("who_are_the_stakeholders")}
    Expected Deliverables: {data.get("what_are_the_expected_deliverables")}
    Estimated Timeline: {data.get("what_is_the_estimated_timeline")}
    Constraints, Assumptions, and Limitations: {data.get("any_constraints_assumptions_or_limitations")}
    """

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})
    except Exception as e:
        print(e)
        return jsonify({"reply": "❌ Something went wrong."}), 500

if __name__ == "__main__":
    app.run(debug=True)
