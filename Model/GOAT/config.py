# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys and environment variables from environment or .env file
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY', '')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', '')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2', 'false')
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
