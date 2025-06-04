import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

# Initialize OpenAI client properly with v2
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"  # still safe to explicitly set
)

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
        thread = client.beta.threads.create()

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
            instructions="Eres un historiador experto."
        )

        # Poll until run completes
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break

        # Add the message
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # Fetch messages after completion
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_reply = messages.data[0].content[0].text.value

        return jsonify({"reply": assistant_reply})

    except Exception as e:
        print("⚠️ Backend error:", str(e))
        return jsonify({"reply": "Hubo un error al procesar la respuesta."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

