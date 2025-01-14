# backend/test_openai.py

from openai import OpenAI
import json
from app.core.config import settings  # Adjust the import path if necessary
import logging

# Configure Logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture detailed logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_openai_api():
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ],
            temperature=0.7,
            max_tokens=50,
            n=1,
        )

        logger.debug("Response received from OpenAI:")
        logger.debug(response)

        parsed_content = response.choices[0].message.content.strip()
        logger.debug("\nParsed Content:")
        logger.debug(parsed_content)

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    test_openai_api()

