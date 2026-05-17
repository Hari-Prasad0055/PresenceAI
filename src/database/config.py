import streamlit as st
import httpx
from supabase import create_client, Client

# Older supabase-py versions don't expose ClientOptions.
# We work around ReadTimeout by injecting a custom httpx client with a longer timeout.
try:
    from supabase import ClientOptions
    _options = ClientOptions(postgrest_client_timeout=60)
    supabase: Client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
        options=_options,
    )
except (ImportError, TypeError):
    # Fallback for older supabase-py that accepts http_client kwarg
    try:
        _http = httpx.Client(timeout=60.0)
        supabase: Client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"],
            http_client=_http,
        )
    except TypeError:
        # Absolute fallback — no timeout config available, use defaults
        supabase: Client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"],
        )