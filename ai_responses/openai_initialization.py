from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
openaiClient = OpenAI(api_key=api_key)

