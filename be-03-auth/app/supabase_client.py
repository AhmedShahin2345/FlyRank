from supabase import create_client

from . import config

supabase = None


def init_client():
    global supabase
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    return supabase