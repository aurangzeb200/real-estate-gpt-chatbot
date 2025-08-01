# 🏡 AI-Powered Real Estate Chatbot

A multi-channel AI chatbot built with OpenAI GPT-4o that helps users search, explore, and inquire about real estate listings across the U.S.

## 📌 Features

- 🔍 Natural language property search (GPT-4o + SQL)
- 🏢 Building insights (maintenance, fees, issues)
- 📱 Twilio integration for SMS/WhatsApp
- 🧠 Memory support (user follow-ups, reminders)
- 💬 Structured + human-readable responses
- 📦 Secure Microsoft SQL Server backend

## 🛠️ Tech Stack

- Python + FastAPI
- OpenAI GPT-4o (Function Calling)
- Microsoft SQL Server
- Twilio (SMS & WhatsApp)
- pyodbc, pydantic, dotenv


## 🧪 Sample Prompt

> "Show me condos under $900k in downtown LA."

Bot will:
- Run safe SQL query
- Return top 10 matches
- Format human + JSON response

## 🚀 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourname/real-estate-gpt-chatbot.git
cd real-estate-gpt-chatbot


# Install dependencies
pip install -r requirements.txt

# Add your config
# Fill in OpenAI Key, Twilio credentials, and DB connection

# Run server
uvicorn main:app --reload
