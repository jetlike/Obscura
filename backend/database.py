from supabase import create_client
import os
from dotenv import load_dotenv

# Load .env file explicitly, pointing to the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# Get Supabase URL and Key from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("Error: SUPABASE_URL or SUPABASE_KEY is missing.")

# =======================
# Interactions with banned_words Table
# =======================

def insert_banned_word(word: str):
    """
    Insert a new banned word into the banned_words table, ensuring no duplicates
    and that the word length does not exceed the allowed limit.
    """
    # Check if the word length exceeds the limit (255 characters)
    if len(word) > 255:
        print(f"Failed to insert '{word}': Word exceeds maximum length of 255 characters.")
        return

    # Check if the word already exists in the banned_words table
    existing_words = supabase.table("banned_words").select("word").eq("word", word).execute()
    
    # If the word already exists, print an error and return
    if existing_words.data:
        print(f"Failed to insert '{word}': Word already exists.")
        return

    # Proceed with the insertion if no duplicates are found and length is valid
    data = {"word": word}
    response = supabase.table("banned_words").insert(data).execute()
    
    # Check if the insertion was successful and provide feedback
    if response.data:
        print(f"Successfully inserted '{word}' into banned_words table.")
    else:
        print(f"Failed to insert '{word}': {response.data}")



def get_banned_words():
    """
    Retrieve all banned words from the banned_words table.
    """
    response = supabase.table("banned_words").select("*").execute()
    if response.data:
        return response.data
    else:
        print(f"Failed to retrieve banned words: {response.data}")
        return []

def delete_banned_word(word: str):
    """
    Delete a banned word from the banned_words table.
    """
    response = supabase.table("banned_words").delete().eq("word", word).execute()
    if response.data:
        print(f"Successfully deleted {word} from banned_words table.")
    else:
        print(f"Failed to delete {word}: {response.data}")

# =======================
# Interactions with company_settings Table
# =======================

def insert_company(company_name: str, api_key: str, custom_banned_words: list):
    """
    Insert a new company into the company_settings table.
    """
    data = {
        "company_name": company_name,
        "api_key": api_key,
        "custom_banned_words": custom_banned_words,
    }
    response = supabase.table("company_settings").insert(data).execute()
    if response.data:
        print(f"Successfully inserted company {company_name}.")
    else:
        print(f"Failed to insert company {company_name}: {response.data}")

def get_company_by_api_key(api_key: str):
    """
    Retrieve a company from company_settings by API key.
    """
    response = supabase.table("company_settings").select("*").eq("api_key", api_key).execute()
    if response.data:
        return response.data
    else:
        print(f"Failed to retrieve company: {response.data}")
        return []

def update_company_banned_words(company_id: int, custom_banned_words: list):
    """
    Update the custom banned words list for a company in the company_settings table.
    """
    data = {
        "custom_banned_words": custom_banned_words
    }
    response = supabase.table("company_settings").update(data).eq("company_id", company_id).execute()
    if response.data:
        print(f"Successfully updated banned words for company {company_id}.")
    else:
        print(f"Failed to update banned words for company {company_id}: {response.data}")

def delete_company(company_id: int):
    """
    Delete a company from the company_settings table.
    """
    response = supabase.table("company_settings").delete().eq("company_id", company_id).execute()
    if response.data:
        print(f"Successfully deleted company with ID {company_id}.")
    else:
        print(f"Failed to delete company with ID {company_id}: {response.data}")

# =======================
# Interactions with flagged_messages Table
# =======================

def insert_flagged_message(company_id: int, uncensored_message: str, censored_message: str, censored_words: list):
    """
    Insert a flagged message into the flagged_messages table.
    """
    data = {
        "company_id": company_id,
        "uncensored_message": uncensored_message,
        "censored_message": censored_message,
        "censored_words": censored_words,
    }
    response = supabase.table("flagged_messages").insert(data).execute()
    if response.data:
        print(f"Successfully inserted flagged message for company {company_id}.")
    else:
        print(f"Failed to insert flagged message: {response.data}")

def get_flagged_messages(company_id: int):
    """
    Retrieve all flagged messages for a given company from the flagged_messages table.
    """
    response = supabase.table("flagged_messages").select("*").eq("company_id", company_id).execute()
    if response.data:
        return response.data
    else:
        print(f"Failed to retrieve flagged messages for company {company_id}: {response.data}")
        return []

def get_flagged_message_by_id(message_id: int):
    """
    Retrieve a flagged message by its message_id from the flagged_messages table.
    """
    response = supabase.table("flagged_messages").select("*").eq("message_id", message_id).execute()
    if response.data:
        return response.data
    else:
        print(f"Failed to retrieve flagged message by ID: {response.data}")
        return None

def update_flagged_message_status(message_id: int, censored_message: str, censored_words: list):
    """
    Update a flagged message's censored version and the list of censored words.
    """
    data = {
        "censored_message": censored_message,
        "censored_words": censored_words
    }
    response = supabase.table("flagged_messages").update(data).eq("message_id", message_id).execute()
    if response.data:
        print(f"Successfully updated flagged message {message_id}.")
    else:
        print(f"Failed to update flagged message {message_id}: {response.data}")

def delete_flagged_message(message_id: int):
    """
    Delete a flagged message from the flagged_messages table.
    """
    response = supabase.table("flagged_messages").delete().eq("message_id", message_id).execute()
    if response.data:
        print(f"Successfully deleted flagged message with ID {message_id}.")
    else:
        print(f"Failed to delete flagged message with ID {message_id}: {response.data}")

### DONT RUN THIS LIKE EVER, ONLY USED FOR BASE LEVEL TESTING WHEN I SET UP THE PROJECT
########################
def delete_all_data():
    """
    Deletes all data from the banned_words, company_settings, and flagged_messages tables.
    """
    try:
        # Delete all records from banned_words
        banned_words_response = supabase.table("banned_words").delete().eq("id", 1).execute()  # Just needs to pass a condition
        print(banned_words_response.data)
        if banned_words_response.data is not None:
            print("Successfully deleted all records from banned_words.")
        else:
            print("Failed to delete records from banned_words.")

        # Delete all records from company_settings
        company_settings_response = supabase.table("company_settings").delete().eq("company_id", 1).execute()
        if company_settings_response.data is not None:
            print("Successfully deleted all records from company_settings.")
        else:
            print("Failed to delete records from company_settings.")

        # Delete all records from flagged_messages
        flagged_messages_response = supabase.table("flagged_messages").delete().eq("message_id", 1).execute()
        if flagged_messages_response.data is not None:
            print("Successfully deleted all records from flagged_messages.")
        else:
            print("Failed to delete records from flagged_messages.")

    except Exception as e:
        print(f"Error during deletion: {e}")