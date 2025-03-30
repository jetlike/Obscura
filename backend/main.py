from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from filter import check_profanity
from database import insert_company, get_company_by_name, generate_api_key, get_flagged_messages, get_company_by_api_key

app = FastAPI()

# Define user registration
class UserRegistration(BaseModel):
    name: str
    custom_banned_words: list[str]
    
@app.post("/register")
async def register_company(company: UserRegistration):
    # Check if company with the same API key already exists
    existing_company = get_company_by_name(company.name)
    if existing_company:
        raise HTTPException(status_code=400, detail="Company with this API key already exists.")
    
    # Generate a new unique API key
    api_key = generate_api_key()
    
    # Register the company
    insert_company(company.name, api_key, company.custom_banned_words)
    return {"message": "Company registered successfully"}

# Define input model
class TextInput(BaseModel):
    text: str
    api_key: str  # Add API key to input data

@app.post("/moderate")
def moderate_text(input_text: TextInput):
    # Check profanity and return censored text and flagged words
    result = check_profanity(input_text.text, input_text.api_key)

    # If error occurs (e.g., invalid API key), raise an exception
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result  # FastAPI automatically formats this as JSON

@app.get("/company-stats")
async def get_company_stats(api_key: str):
    # Get company data using API key
    company = get_company_by_api_key(api_key)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    company_id = company["company_id"]
    
    # Fetch flagged messages for the company
    flagged_messages = get_flagged_messages(company_id)
    
    return {"company": company["company_name"], "flagged_messages": flagged_messages}
