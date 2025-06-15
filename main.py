from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_query = req.get("queryResult", {}).get("queryText", "")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_query}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"fulfillmentText": "Oops, something went wrong!"})

    return jsonify({"fulfillmentText": reply})
