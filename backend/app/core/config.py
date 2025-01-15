# app/core/config.py

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
    SUPABASE_ANON_KEY: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Standard column mappings
    STANDARD_COLUMNS: Dict[str, List[str]] = {
        "Export Invoice #": ["Export Invoice #", "Export Document", "Export Invoice Number", "Invoice Number", "Invoice #"],
        "Product Code": ["Style", "Item", "Product Style", "Style/Item/Style/Product Style", "Product Code", "Style Code"],
        "Description": ["Description", "Item Description", "Product Description", "desc", "product_desc", "item_description"],
        "Invoice Quantity": ["Quantity", "QTY", "Invoice Qty", "Qty", "quantity", "Invoice Quantity"],
        "Total Amount": ["Total Amount", "Amount US$", "Amount", "Total", "total", "total_price", "amount", "Price"],
        "HS Code": ["HS Code", "Customs Nomenclature", "Tariff Code", "HTS", "Harmonized Code"],
        # "Customs Unit of Measure" and "Customs Quantity" will be derived fields
    }

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
