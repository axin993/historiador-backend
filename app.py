import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = "https://api.openai.com/v1"

# Load Assistant ID
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Setup Flask app and CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
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

    except Exception as e:
        print("⚠️ Backend error:", str(e))
        return jsonify({"reply": "Hubo un error al procesar la respuesta."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

