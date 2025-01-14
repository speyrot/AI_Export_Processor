# app/core/supabase.py

from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from .config import settings

def init_supabase() -> Client:
    options = ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
        headers={
            'Authorization': f'Bearer {settings.SUPABASE_SERVICE_KEY}',
            'apikey': settings.SUPABASE_SERVICE_KEY
        }
    )
    
    supabase = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY,
        options=options
    )
    return supabase

supabase = init_supabase() 