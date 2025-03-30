from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from filter import normalize_leetspeak, check_profanity

app = FastAPI()

# Define input model
class TextInput(BaseModel):
    text: str
    api_key: str  # Add API key to input data

@app.post("/moderate")
def moderate_text(input_text: TextInput):
    # Normalize leetspeak
    normalized_text = normalize_leetspeak(input_text.text)

    # Check profanity and return censored text and flagged words
    result = check_profanity(normalized_text, input_text.api_key)

    # If error occurs (e.g., invalid API key), raise an exception
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result  # FastAPI automatically formats this as JSON
