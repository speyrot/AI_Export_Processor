from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .services.processing import process_invoice
from .core.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    fileUrl: str
    userId: str
    originalFileName: str

@app.post("/api/process")
async def process_file(request: ProcessRequest):
    """
    Process an invoice file from Supabase storage.
    Returns the URL where the processed file can be downloaded.
    """
    try:
        logger.info(f"Processing request: {request}")
        
        processed_file_url = await process_invoice(
            request.fileUrl,
            request.userId,
            request.originalFileName
        )
        return {"fileUrl": processed_file_url}
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 