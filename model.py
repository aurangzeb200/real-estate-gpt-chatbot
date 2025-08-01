from google import genai
from google.genai import types 
from prompt import system_prompt
from sql_util import run_sql
from dotenv import load_dotenv
import os
import asyncio
from memory import CONVERSATION_FILE

load_dotenv()


async def get_text_from_response(response):
    """Extracts text from a Gemini response, ignoring non-text parts to avoid warnings."""
    return "".join((part.text or "") for part in response.candidates[0].content.parts if hasattr(part, "text"))


async def run_sql_query(query: str):
    """
    Executes SQL queries on the RealEstate database.
    Args:
        query: The SQL query to be executed.
    Returns:
        String 
    """
    return await run_sql(query)


sql_generator_function = {
    "name": "run_sql_query",
    "description": "Use this function to execute a SQL query on the RealEstateDB database when the user asks for specific data about properties, agents, or buyers.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",   
                "description": "The SQL query to be executed",
            },
        },
        "required": ["query"],
    },
}

tools=types.Tool(function_declarations=[sql_generator_function])


def get_conversation_history():
    """
    Reads the conversation history from conversation.txt and returns it as a string.
    """
    if not os.path.exists(CONVERSATION_FILE):
        return ""
    with open(CONVERSATION_FILE, "r", encoding="utf-8") as f:
        return f.read()


async def chat_with_model(prompt : str):
    history = get_conversation_history()
    if history:
        full_prompt = "Converstaion History:\n" + history + f"\n\n\nUser asked this now: {prompt}\n"
    else:
        full_prompt = prompt
    contents = [
    types.Content(role="user", parts=[types.Part(text=full_prompt)]),
]

    client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

    gemini_response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents = contents,
        config=types.GenerateContentConfig(
            tools=[tools],
            system_instruction=system_prompt
        )
    )

    tool_call = gemini_response.candidates[0].content.parts[0].function_call
    if tool_call and tool_call.name == "run_sql_query":
        result = await run_sql_query(**tool_call.args)

        function_response_part = types.Part.from_function_response(
            name=tool_call.name,
            response={"result": result},
        )

        contents.append(gemini_response.candidates[0].content) 
        contents.append(types.Content(role="user", parts=[function_response_part])) 

        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[tools]
            ),
            contents=contents,
        )
        return await get_text_from_response(final_response)
    
    else:
        return await get_text_from_response(gemini_response)
    
# print(chat_with_model("show me houses having 2 bathrooms"))