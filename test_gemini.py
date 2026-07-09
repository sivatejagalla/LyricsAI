import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send a simple prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello! Tell me one interesting fact about music."
)

print(response.text)