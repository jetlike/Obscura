import re
from database import get_banned_words, insert_flagged_message,  get_company_by_api_key

# Leetspeak normalization
LEETSPEAK_MAP = {
    "@": "a", "$": "s", "0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t",
    "\\/\\/": "w", # w must come first because technically n is contained within w
    "/\\/": "n"  # Use raw string to escape backslashes correctly
    
}

# this method is supposed to like normalize weird characters into normal letters, but depending on like the context based shit or ai shit you might not need this
def normalize_leetspeak(text: str) -> str:
    """
    Normalize leetspeak characters in the text to their normal alphabetic equivalents.
    """
    print(text)
    for leet, normal in LEETSPEAK_MAP.items():
        text = text.replace(leet, normal)
    print(text)
    return text

def check_profanity(text: str, api_key: str) -> dict:
    """
    Checks for profanity in the text based on global and company-specific banned words.
    Returns the censored text and logs flagged messages for analytics.
    """
    # Get company settings using the API key
    company_data = get_company_by_api_key(api_key)
    
    if not company_data:
        return {"error": "Invalid API key"}

    company_id = company_data[0]["company_id"]
    custom_banned_words = set(company_data[0].get("custom_banned_words", []))

    # Fetch global banned words and merge with company-specific ones
    global_banned_words = {entry["word"] for entry in get_banned_words()}
    banned_words = global_banned_words.union(custom_banned_words)

    # Normalize the text to account for leetspeak
    normalized_text = normalize_leetspeak(text)

    # Detect and censor banned words
    words = normalized_text.split()
    flagged_words = [word for word in words if word.lower() in banned_words]
    censored_text = " ".join("*" * len(word) if word.lower() in banned_words else word for word in words)

    # Insert the flagged message into the database for analytics
    if flagged_words:
        insert_flagged_message(company_id, text, censored_text, flagged_words)

    return {"censored_text": censored_text, "flagged_words": flagged_words}
