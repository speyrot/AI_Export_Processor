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
    """
    # Handle None or NaN values
    if pd.isna(invoice_quantity):
        return 0.0

    try:
        invoice_quantity = float(invoice_quantity)
    except (ValueError, TypeError):
        logger.error(f"Invalid invoice quantity: {invoice_quantity}")
        return 0.0

    unit_factors = {
        "DOZ": 12,
        "NUM": 1,
        "KG": 1,
        "LBS": 1,
    }
    factor = unit_factors.get(unit_of_measure, 1)
    
    try:
        return invoice_quantity / factor
    except Exception as e:
        logger.error(f"Error calculating customs quantity: {e}")
        return 0.0

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
        loop = asyncio.get_running_loop()

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
        logger.info("Reading Excel file and identifying headers")
        engine = 'openpyxl' if file_extension == '.xlsx' else 'xlrd'
        df = pd.read_excel(temp_path, engine=engine, header=None)
        
        # Find the row containing 'EAN Code' which indicates our header row
        header_row = None
        for idx, row in df.iterrows():
            if 'EAN Code' in row.values:
                header_row = idx
                break
        
        if header_row is None:
            raise ValueError("Could not find header row with 'EAN Code'")
        
        # Read the file again, but now with the correct header row
        df = pd.read_excel(temp_path, engine=engine, skiprows=header_row)
        
        # Clean up column names (remove any whitespace)
        df.columns = df.columns.str.strip()
        
        logger.info(f"Found headers at row {header_row}")
        logger.info(f"Actual columns found: {df.columns.tolist()}")
        
        # Create the standardized DataFrame with direct mappings
        standardized_df = pd.DataFrame()
        
        # Direct column mappings
        column_mappings = {
            'Style': 'Product Code',
            'Description': 'Description',
            'HS code': 'HS Code',
            'Export Invoice #': 'Export Invoice #',
            'Quantity': 'Invoice Quantity',
            'Total Amount': 'Total Amount'
        }
        
        # Apply the mappings and log each mapping attempt
        for source_col, target_col in column_mappings.items():
            if source_col in df.columns:
                logger.info(f"Mapping column {source_col} to {target_col}")
                standardized_df[target_col] = df[source_col]
            else:
                logger.error(f"Missing column: {source_col}")
                logger.info(f"Available columns: {df.columns.tolist()}")
                standardized_df[target_col] = None
        
        # Add debug logging
        logger.info(f"Original DataFrame sample:\n{df.head()}")
        logger.info(f"Standardized DataFrame sample:\n{standardized_df.head()}")
        
        # Ensure we have data
        if standardized_df.empty:
            raise ValueError("No data was extracted from the file")
        
        # Ensure all required columns are present and have data
        required_columns = [
            "Export Invoice #",
            "Product Code",
            "Description",
            "Invoice Quantity",
            "Total Amount",
            "HS Code"
        ]
        
        missing_columns = [col for col in required_columns if col not in standardized_df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Determine Customs Unit of Measure based on HS Code
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
            "Product Code",
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

        # Determine output format (always save as xlsx)
        output_filename = os.path.splitext(original_filename)[0] + '.xlsx'
        output_path = os.path.join(tempfile.gettempdir(), output_filename)

        try:
            # Save to Excel (xlsx format)
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                standardized_df.to_excel(writer, index=False)
            logger.info(f"Saved processed file to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving Excel file: {e}")
            raise

        # Upload processed file to Supabase
        try:
            with open(output_path, 'rb') as f:
                # Use the uploads folder since we know it works for the initial file
                processed_file_path = f'uploads/{user_id}/processed_{output_filename}'
                logger.info(f"Uploading to Supabase: {processed_file_path}")
                
                # Upload with minimal options
                result = supabase.storage.from_('invoices').upload(
                    path=processed_file_path,
                    file=f
                )
                logger.info(f"Upload successful: {result}")

        except Exception as e:
            logger.error(f"Error uploading to Supabase: {str(e)}")
            raise Exception(f"Failed to upload processed file: {str(e)}")

        # Get signed URL for the processed file
        try:
            signed_url_result = supabase.storage.from_('invoices').create_signed_url(
                path=processed_file_path,
                expires_in=3600
            )
            
            if isinstance(signed_url_result, dict) and 'signedURL' in signed_url_result:
                signed_url = signed_url_result['signedURL']
                logger.info(f"Generated signed URL successfully")
                return signed_url
            else:
                logger.error(f"Unexpected signed URL result format: {signed_url_result}")
                raise Exception("Failed to generate valid signed URL")
        
        except Exception as url_error:
            logger.error(f"Error getting signed URL: {str(url_error)}")
            raise Exception(f"Failed to generate signed URL: {str(url_error)}")

        # Add after the mappings are created:
        logger.info("Original columns:", df.columns.tolist())
        logger.info("Reverse mappings:", reverse_mappings)
        logger.info("Final columns in standardized_df:", standardized_df.columns.tolist())

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
