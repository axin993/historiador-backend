import os
import time
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

# Load Assistant ID from env
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Setup Flask app and CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        # 1️⃣ Create thread
        thread = client.beta.threads.create()

        # 2️⃣ Add user message BEFORE creating run
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # 3️⃣ Now create run AFTER message exists
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # 4️⃣ Poll run status
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            time.sleep(0.5)

        # 5️⃣ Retrieve assistant reply
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_reply = messages.data[0].content[0].text.value

        return jsonify({"reply": assistant_reply})

    except Exception as e:
        print("⚠️ Backend error:", str(e))
        return jsonify({"reply": "Hubo un error al procesar la respuesta."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


