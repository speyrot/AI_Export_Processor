from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Dict, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Invoice Processor"
    API_V1_STR: str = "/api"
    
    # Directory for temporary file storage
    UPLOAD_DIR: str = str(Path("uploads").absolute())
    
    # Supabase settings
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Standard column mappings
    STANDARD_COLUMNS: Dict[str, List[str]] = {
        'Product Code': ['product_code', 'style_code', 'item_code', 'sku'],
        'Description': ['desc', 'product_desc', 'item_description', 'description'],
        'Quantity': ['qty', 'quantity', 'amount'],
        'Unit Price': ['price', 'unit_price', 'rate'],
        'Total': ['total', 'total_price', 'amount']
    }

    class Config:
        env_file = ".env"

settings = Settings() 