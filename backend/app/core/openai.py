from openai import OpenAI
from .config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def get_column_mappings(headers: list[str], standard_columns: dict) -> dict:
    """Use OpenAI to intelligently map source columns to standard columns"""
    
    prompt = f"""
    I have an Excel file with these columns: {', '.join(headers)}
    
    I need to map these to standard columns: {list(standard_columns.keys())}
    
    Each standard column has these common variations:
    {standard_columns}
    
    Return only a JSON object mapping source columns to standard columns.
    Example: {{"source_col1": "Standard Col 1", "source_col2": "Standard Col 2"}}
    """
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that maps Excel columns to standard formats."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    
    return response.choices[0].message.content 