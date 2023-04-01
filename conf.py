import os
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.environ.get('OPENAI_API_KEY')
EXIT_PHRASE = os.environ.get('EXIT_PHRASE')
SYSTEM_CONTENT = os.environ.get('SYSTEM_CONTENT')