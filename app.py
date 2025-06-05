import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import time

# Initialize OpenAI client with v2 API
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

ASSISTANT_ID = os.getenv("ASSISTANT_ID")

app = Flask(__name__)

# 🔧 CORS now restricted to your real frontend domain:
CORS(app, resources={r"/*": {"origins": "https://historiador.vercel.app"}})

# Route to create a new thread
@app.route("/start", methods=["POST"])
def start():
    try:
        thread = client.beta.threads.create()
        return jsonify({"thread_id": thread.id})
    except Exception as e:
        print("⚠️ Error creating thread:", str(e))
        return jsonify({"error": "Failed to create thread."}), 500

# Route to send message inside existing thread
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    thread_id = data.get("thread_id", "")

    try:
        # Add user message to existing thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Poll for run completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            time.sleep(0.5)

        # Get assistant reply
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = messages.data[0].content[0].text.value

        return jsonify({"reply": assistant_reply})

    except Exception as e:
        print("⚠️ Backend error:", str(e))
        return jsonify({"reply": "Hubo un error al procesar la respuesta."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)



