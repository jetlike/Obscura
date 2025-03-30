import re
from unidecode import unidecode
from fuzzywuzzy import fuzz
from database import get_banned_words, insert_flagged_message, get_company_by_api_key
from model2 import predict_severity

def is_similar(word: str, banned_words: set, ratio_threshold: int = 85, partial_threshold: int = 90) -> bool:
    """
    Uses both fuzzy matching ratios to detect close variations of banned words.
    Primary: fuzz.ratio
    Secondary: fuzz.partial_ratio
    """
    for banned_word in banned_words:
        ratio_score = fuzz.ratio(word.lower(), banned_word)
        partial_score = fuzz.partial_ratio(word.lower(), banned_word)

        # First, check if the full string similarity is above the threshold
        if ratio_score >= ratio_threshold:
            return True
        # If the ratio check fails, check the partial string similarity
        if partial_score >= partial_threshold:
            return True

    return False


def check_profanity(text: str, api_key: str) -> dict:
    """
    Checks for profanity using AI-driven transformations, leetspeak normalization, 
    spacing normalization, and fuzzy matching.
    """
    company_data = get_company_by_api_key(api_key)
    if not company_data:
        return {"error": "Invalid API key"}

    company_id = company_data["company_id"]
    company_severity = company_data["profanity_tolerance"]
    custom_banned_words = set(company_data.get("custom_banned_words", []))

    # Fetch global banned words and merge with company-specific ones
    global_banned_words = {entry["word"] for entry in get_banned_words()}
    banned_words = global_banned_words.union(custom_banned_words)

    # Step 1: Split the text into words and punctuation while keeping punctuation intact
    words_and_punct = re.findall(r'[a-zA-Z0-9_\-\/\\|]+|[^\w\s]+', text)

    flagged_words = []  # This needs to be defined before usage
    censored_text = text  # Initialize censored_text with original text

    # Step 2: Censor words and keep punctuation intact
    for word in words_and_punct:
        print(word)
        # Get the severity score first
        model_output = predict_severity(word)
        severity = model_output["severity"]
        print(severity)
        normalized_word = model_output["normalized"]
        # Skip this word if its severity is below the company threshold
        if severity < company_severity:
            continue  # Skip processing for words that don't meet the severity threshold

        # If the word is in banned words, add it to flagged_words and censor it
        if normalized_word.lower() in banned_words:
            flagged_words.append(normalized_word.lower())  # Exact match
            censored_text = censored_text.replace(word, "*" * len(word))  # Censor word

        # If the word is similar to a banned word, find the matched banned word and censor it
        elif is_similar(normalized_word.lower(), banned_words):
            matched_word = next(banned_word for banned_word in banned_words 
                if (fuzz.ratio(normalized_word.lower(), banned_word) >= 85 or fuzz.partial_ratio(normalized_word.lower(), banned_word) >= 90))
            flagged_words.append(matched_word.lower())  # Fuzzy match
            censored_text = censored_text.replace(word, "*" * len(word))  # Censor word

    # Step 3: Log flagged messages
    if flagged_words:
        insert_flagged_message(company_id, text, censored_text, flagged_words)

    # Return censored text and flagged words
    return {"censored_text": censored_text, "flagged_words": flagged_words}
