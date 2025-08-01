from fastapi import APIRouter, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
from fastapi.responses import Response
from model import chat_with_model
import asyncio
from memory import store_conversation

router = APIRouter()

@router.post("/webhook/twilio")
async def incoming_message(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):

    query = Body
    gemini_text = await chat_with_model(query)
    store_conversation(query, gemini_text)

    twilio_response = MessagingResponse()
    twilio_response.message(gemini_text)

    return Response(content=str(twilio_response), media_type="application/xml")
