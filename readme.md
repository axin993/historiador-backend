# Historiador AI Backend

This is the backend server for the Historiador AI project — your custom GPT-powered assistant that debates the historical foundation of Guayaquil!

It uses:
- Flask (Python backend)
- OpenAI Assistants API
- Railway (for backend hosting)
- Vercel (for frontend hosting — coming soon!)

---

## ✅ Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main backend server (Flask app) |
| `requirements.txt` | Dependencies list |
| `.env.sample` | Environment variables template |
| `README.md` | Setup guide (this file) |

---

## 🚀 Local Development Setup

### 1️⃣ Clone your repository

```bash
git clone <your-repo-url>
cd historiador-backend

2️⃣ (Optional but recommended) Create virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Create a .env file locally

Use .env.sample as a reference. Inside .env, place your real API keys:

OPENAI_API_KEY=your_real_openai_api_key
ASSISTANT_ID=your_real_assistant_id

5️⃣ Run the app locally

python app.py

Server will run on http://localhost:5000
🚀 Deployment to Railway (Production)

1️⃣ Login to Railway

2️⃣ Deploy from GitHub Repo

    Select Deploy from GitHub repo

    Choose this repository

3️⃣ Set Environment Variables in Railway:
Variable	Value
OPENAI_API_KEY	(your real OpenAI key)
ASSISTANT_ID	(your Historiador Assistant ID)

4️⃣ Click Deploy
🚀 Frontend

The frontend client will connect to this backend. Coming soon in the next step!
🤖 Notes

    You never commit your real .env file to GitHub.

    The .env.sample helps future developers know which keys are required.