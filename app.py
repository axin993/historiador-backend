import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = "https://api.openai.com/v1"

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
    # Get PORT from environment (Render will inject it)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
