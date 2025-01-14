# app/services/processing.py

import pandas as pd
from ..core.config import settings
from ..core.supabase import supabase
from ..core.openai_client import get_column_mappings, get_unit_of_measure_cached
import tempfile
import os
from datetime import datetime
import logging
import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# Create a ThreadPoolExecutor for running synchronous functions
executor = ThreadPoolExecutor(max_workers=10)

def calculate_customs_quantity(invoice_quantity: float, unit_of_measure: str) -> float:
    """
    Calculate Customs Quantity based on Invoice Quantity and Unit of Measure.

    Args:
        invoice_quantity (float): The quantity from the invoice.
        unit_of_measure (str): The customs unit of measure abbreviation.

    Returns:
        float: The calculated customs quantity.
    """
    unit_factors = {
        "DOZ": 12,
        "NUM": 1,
        "KG": 1,    # Assuming per kilogram
        "LBS": 1,   # Assuming per pound
        # Add more unit factors as needed
    }
    factor = unit_factors.get(unit_of_measure, 1)
    try:
        return invoice_quantity / factor
    except Exception as e:
        logger.error(f"Error calculating customs quantity: {e}")
        return invoice_quantity  # Fallback to invoice quantity if error occurs

async def process_invoice(file_url: str, user_id: str, original_filename: str) -> str:
    """
    Process an invoice file from Supabase storage and return the URL of the processed file.

    Args:
        file_url (str): The signed URL of the original invoice file.
        user_id (str): The ID of the user processing the file.
        original_filename (str): The original filename of the invoice.

    Returns:
        str: The public URL of the processed invoice file.
    """
    logger.info(f"Starting to process file: {file_url}")

    try:
        # Download file using the signed URL directly
        async with httpx.AsyncClient() as client_http:
            logger.info("Downloading from signed URL")
            response = await client_http.get(file_url)
            response.raise_for_status()
            file_content = response.content

        # Determine file extension
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

        # Get AI-powered column mappings using run_in_executor
        logger.info("Getting column mappings")
        loop = asyncio.get_event_loop()
        mappings = await loop.run_in_executor(
            executor,
            get_column_mappings,
            df.columns.tolist(),
            settings.STANDARD_COLUMNS
        )
        logger.info(f"Column mappings: {mappings}")

        # Validate that all required standard columns are mapped
        required_columns = ["Export Invoice #", "Style", "Description", "Invoice Quantity", "Total Amount", "HS Code"]
        missing_columns = [col for col in required_columns if col not in mappings.values()]
        if missing_columns:
            raise ValueError(f"Missing required columns after mapping: {missing_columns}")

        # Apply mappings to create standardized DataFrame
        standardized_df = pd.DataFrame()
        for source_col, standard_col in mappings.items():
            if source_col in df.columns and standard_col in required_columns:
                standardized_df[standard_col] = df[source_col]

        # Ensure all required columns are present
        for col in required_columns:
            if col not in standardized_df.columns:
                standardized_df[col] = None  # or handle as appropriate

        # Determine Customs Unit of Measure based on HS Code using run_in_executor
        logger.info("Determining Customs Unit of Measure based on HS Code")
        hs_codes = standardized_df['HS Code'].astype(str).unique().tolist()

        # Create a mapping from HS Code to Unit of Measure using the cached function
        tasks = []
        for hs in hs_codes:
            tasks.append(loop.run_in_executor(
                executor,
                get_unit_of_measure_cached,
                hs
            ))
        units = await asyncio.gather(*tasks)
        hs_to_unit = dict(zip(hs_codes, units))

        # Apply the HS Code to Unit of Measure mapping
        standardized_df['Customs Unit of Measure'] = standardized_df['HS Code'].astype(str).map(hs_to_unit)

        # Calculate Customs Quantity
        logger.info("Calculating Customs Quantity")
        standardized_df['Customs Quantity'] = standardized_df.apply(
            lambda row: calculate_customs_quantity(row['Invoice Quantity'], row['Customs Unit of Measure']),
            axis=1
        )

        # Select and order the required columns
        output_columns = [
            "Export Invoice #",
            "Style",
            "Description",
            "Invoice Quantity",
            "Total Amount",
            "Customs Unit of Measure",
            "Customs Quantity",
            "HS Code"
        ]
        standardized_df = standardized_df[output_columns]

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
        file_url_processed = supabase.storage.from_('invoices').get_public_url(processed_file_path)
        logger.info(f"Generated public URL: {file_url_processed}")

        return file_url_processed

    except Exception as e:
        logger.error(f"Error in processing: {str(e)}", exc_info=True)
        raise
    finally:
        # Clean up temporary files
        try:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            if 'output_path' in locals() and os.path.exists(output_path):
                os.unlink(output_path)
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {str(e)}")
