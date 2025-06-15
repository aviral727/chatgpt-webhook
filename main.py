from flask import Flask, request, jsonify
import openai
import os

my_secret = os.environ['ChatGptApiKey']

app = Flask(__name__)

openai.api_key = my_secret


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_query = req["queryResult"]["queryText"]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{
                                                "role": "user",
                                                "content": user_query
                                            }])

    chat_response = response["choices"][0]["message"]["content"]

    return jsonify({"fulfillmentText": chat_response})


app.run(host="0.0.0.0", port=5001)
