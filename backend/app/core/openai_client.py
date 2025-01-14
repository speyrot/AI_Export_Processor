# app/core/openai_client.py

from openai import OpenAI
import json
from typing import List, Dict
from functools import lru_cache
from tenacity import retry, wait_exponential, stop_after_attempt
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Instantiate the OpenAI client correctly
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_unit_of_measure(hs_code: str) -> str:
    """
    Use OpenAI to determine the customs unit of measure based on the HS Code.

    Args:
        hs_code (str): The HS Code from the invoice.

    Returns:
        str: The customs unit of measure abbreviation (e.g., DOZ, NUM).
    """
    prompt = f"""
    Given the HS Code: {hs_code}, determine the appropriate Customs Unit of Measure (e.g., Dozen (DOZ), Number (NUM), etc.).

    Provide only the unit abbreviation (e.g., DOZ, NUM).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that determines the customs unit of measure based on HS Codes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10,
            n=1,
        )

        logger.debug(f"Raw response from OpenAI for HS Code '{hs_code}': {response}")

        unit = response.choices[0].message.content.strip().upper()

        # Simple validation to ensure it's an abbreviation
        if len(unit) > 5 or not unit.isalpha():
            # Default to 'NUM' if the response is unexpected
            logger.warning(f"Unexpected unit format '{unit}' for HS Code '{hs_code}'. Defaulting to 'NUM'.")
            unit = "NUM"

        return unit

    except Exception as e:
        logger.error(f"Error during OpenAI API call for HS Code '{hs_code}': {e}")
        raise

@lru_cache(maxsize=1024)
def get_unit_of_measure_cached(hs_code: str) -> str:
    """
    Cached version of get_unit_of_measure to reduce API calls.

    Args:
        hs_code (str): The HS Code from the invoice.

    Returns:
        str: The customs unit of measure abbreviation.
    """
    return get_unit_of_measure(hs_code)

def get_column_mappings(headers: List[str], standard_columns: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Use OpenAI to intelligently map source Excel columns to standard columns.

    Args:
        headers (List[str]): List of column headers from the source Excel file.
        standard_columns (Dict[str, List[str]]): Dictionary mapping standard columns to their possible variations.

    Returns:
        Dict[str, str]: A dictionary mapping source columns to standard columns.
    """
    # Prepare variations for prompt
    variations = "\n".join([f"{standard}: {', '.join(variants)}" for standard, variants in standard_columns.items()])

    prompt = f"""
    I have an Excel file with these columns: {', '.join(headers)}.

    I need to map these to the following standard columns: {', '.join(standard_columns.keys())}.

    Different customers may use different names for the same data. Below are the standard columns and their possible variations:

    {variations}

    Map each source column to the appropriate standard column. If a source column does not match any standard column, it can be ignored.

    Return only a JSON object mapping source columns to standard columns.

    Example:
    {{"source_col1": "Export Invoice #", "source_col2": "Style"}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that maps Excel columns to standard formats."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,  # For deterministic output
            max_tokens=300,
            n=1,
        )

        logger.debug(f"Raw response from OpenAI for column mappings: {response}")

        raw_content = response.choices[0].message.content.strip()
        logger.debug(f"Raw content for JSON parsing: '{raw_content}'")

        mappings = json.loads(raw_content)
        logger.debug(f"Parsed mappings: {mappings}")

        return mappings

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from OpenAI: {e}. Raw content: '{raw_content}'")
        # Implement fallback: attempt to parse manually or return a default mapping
        # For example, return a direct mapping based on standard_columns
        fallback_mappings = {}
        for col in headers:
            for standard, variants in standard_columns.items():
                if col in variants:
                    fallback_mappings[col] = standard
                    break
        logger.info(f"Using fallback mappings: {fallback_mappings}")
        return fallback_mappings

    except Exception as e:
        logger.error(f"Unexpected error during OpenAI API call for column mappings: {e}")
        raise
