from fastapi import FastAPI
from twilio_webhook import router as twilio_router

app = FastAPI()

# Mount the Twilio webhook
app.include_router(twilio_router)
