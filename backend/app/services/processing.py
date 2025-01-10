import pandas as pd
from ..core.config import settings
from ..core.supabase import supabase
from ..core.openai import get_column_mappings
import tempfile
import os
from datetime import datetime
import logging
import io
import httpx

logger = logging.getLogger(__name__)

async def process_invoice(file_url: str, user_id: str, original_filename: str) -> str:
    """
    Process an invoice file from Supabase storage and return the URL of the processed file.
    """
    logger.info(f"Starting to process file: {file_url}")
    
    try:
        # Download file using the signed URL directly
        async with httpx.AsyncClient() as client:
            logger.info(f"Downloading from signed URL")
            response = await client.get(file_url)
            response.raise_for_status()
            file_content = response.content
        
        # Save to temporary file with correct extension
        file_extension = '.xlsx' if original_filename.endswith('.xlsx') else '.xls'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name
            logger.info(f"Saved temporary file to: {temp_path}")
    
        # Read the Excel file with appropriate engine
        logger.info("Reading Excel file")
        engine = 'openpyxl' if file_extension == '.xlsx' else 'xlrd'
        df = pd.read_excel(temp_path, engine=engine)
        logger.info(f"Excel file columns: {df.columns.tolist()}")
        
        # Get AI-powered column mappings
        logger.info("Getting column mappings")
        mappings = await get_column_mappings(
            headers=df.columns.tolist(),
            standard_columns=settings.STANDARD_COLUMNS
        )
        logger.info(f"Column mappings: {mappings}")
        
        # Apply mappings to create standardized DataFrame
        standardized_df = pd.DataFrame()
        for source_col, standard_col in mappings.items():
            if source_col in df.columns:
                standardized_df[standard_col] = df[source_col]
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"processed_{timestamp}_{original_filename}"
        
        # Save to temporary file
        output_path = os.path.join(tempfile.gettempdir(), output_filename)
        standardized_df.to_excel(output_path, index=False)
        logger.info(f"Saved processed file to: {output_path}")
        
        # Upload processed file to Supabase
        try:
            with open(output_path, 'rb') as f:
                processed_file_path = f'processed/{user_id}/{output_filename}'
                logger.info(f"Uploading to Supabase: {processed_file_path}")
                result = supabase.storage.from_('invoices').upload(processed_file_path, f)
                logger.info(f"Upload result: {result}")
        except Exception as e:
            logger.error(f"Error uploading to Supabase: {str(e)}")
            raise Exception(f"Failed to upload processed file: {str(e)}")
        
        # Get public URL for processed file
        file_url = supabase.storage.from_('invoices').get_public_url(processed_file_path)
        logger.info(f"Generated public URL: {file_url}")
        
        return file_url
        
    except Exception as e:
        logger.error(f"Error in processing: {str(e)}", exc_info=True)
        raise
    finally:
        # Clean up temporary files
        try:
            if 'temp_path' in locals():
                os.unlink(temp_path)
            if 'output_path' in locals():
                os.unlink(output_path)
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {str(e)}") 