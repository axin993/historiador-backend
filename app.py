import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Allow frontend access

# Load Assistant ID
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["message"]

    # Create thread
    thread = openai.beta.threads.create()

    # Run assistant
    run = openai.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
        messages=[{"role": "user", "content": user_message}]
    )

    # Get response
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    assistant_reply = messages.data[0].content[0].text.value

    return jsonify({"reply": assistant_reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
