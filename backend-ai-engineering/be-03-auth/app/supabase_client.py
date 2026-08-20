from supabase import create_client

from . import config

_supabase = None


def get_supabase():
    global _supabase
    if _supabase is None:
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        _supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    return _supabase


def init_client():
    return get_supabase()


class _SupabaseProxy:
    def __getattr__(self, name):
        client = get_supabase()
        return getattr(client, name)


supabase = _SupabaseProxy()
