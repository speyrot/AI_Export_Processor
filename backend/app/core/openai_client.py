# app/core/openai_client.py

from openai import OpenAI
import json
from typing import List, Dict
from functools import lru_cache
from tenacity import retry, wait_exponential, stop_after_attempt
from .config import settings
import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Instantiate the OpenAI client correctly
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_unit_of_measure(hs_code: str) -> str:
    """
    Use OpenAI to determine the customs unit of measure based on the HS Code.
    """
    if not hs_code or pd.isna(hs_code):
        return "NUM"  # Default to NUM if no HS code

    prompt = f"""
    For HS Code '{hs_code}', provide ONLY the standard customs unit of measure abbreviation.
    Use one of: NUM (Number), DOZ (Dozen), KG (Kilogram), LBS (Pounds).
    Respond with ONLY the abbreviation.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a customs unit of measure assistant. Respond only with unit abbreviations: NUM, DOZ, KG, or LBS."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10,
            n=1,
        )

        unit = response.choices[0].message.content.strip().upper()
        
        # Validate the response is one of our accepted units
        valid_units = {"NUM", "DOZ", "KG", "LBS"}
        if unit not in valid_units:
            logger.warning(f"Unexpected unit format '{unit}' for HS Code '{hs_code}'. Defaulting to 'NUM'.")
            return "NUM"
        
        return unit

    except Exception as e:
        logger.error(f"Error getting unit of measure for HS Code '{hs_code}': {str(e)}")
        return "NUM"  # Default to NUM in case of any errors

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
    """
    # First, try to get the actual content of the first row for unnamed columns
    cleaned_headers = []
    for header in headers:
        # Convert header to string and handle nan values
        header_str = str(header) if not pd.isna(header) else ''
        
        if header_str.startswith('Unnamed:') or header_str == 'nan' or header_str == '':
            cleaned_headers.append(f"Column {len(cleaned_headers) + 1}")
        else:
            cleaned_headers.append(header_str)

    # Prepare variations for prompt
    variations = "\n".join([f"{standard}: {', '.join(variants)}" for standard, variants in standard_columns.items()])

    prompt = f"""
    Task: Map Excel columns to standard column names.

    Source columns: {', '.join(cleaned_headers)}
    Target standard columns: {', '.join(standard_columns.keys())}

    Rules:
    1. Return ONLY a valid JSON object
    2. Map source columns to standard columns based on best match
    3. Use exact matches when possible
    4. Use semantic matching for unclear cases
    5. Include only valid mappings
    6. If no valid mappings are found, return an empty JSON object {{}}

    Example response format:
    {{"source_column1": "Export Invoice #", "source_column2": "Style"}}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a precise data mapping assistant. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=300,
        n=1,
    )

    try:
        mappings = json.loads(response.choices[0].message.content.strip())
        
        # Validate mappings
        valid_mappings = {}
        for source, target in mappings.items():
            if target in standard_columns.keys():
                # Find the original header index from cleaned headers
                try:
                    original_idx = cleaned_headers.index(source)
                    original_header = headers[original_idx]
                    # Convert nan to string representation if needed
                    if pd.isna(original_header):
                        original_header = f"Column {original_idx + 1}"
                    valid_mappings[str(original_header)] = target
                except ValueError:
                    continue
        
        return valid_mappings

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from OpenAI: {e}")
        logger.error(f"Raw content: {response.choices[0].message.content}")
        return {}
