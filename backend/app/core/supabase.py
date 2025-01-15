# app/core/supabase.py

from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from .config import settings

def init_supabase() -> Client:
    options = ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
        headers={
            # Use anon key for storage operations to respect RLS
            'apikey': settings.SUPABASE_ANON_KEY,
            # Include service key in headers for admin operations if needed
            'Authorization': f'Bearer {settings.SUPABASE_SERVICE_KEY}'
        }
    )
    
    # Initialize with anon key for client operations
    supabase = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_ANON_KEY,  # Use anon key as primary
        options=options
    )
    return supabase

supabase = init_supabase() 