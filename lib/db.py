import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_random_jumpable_site():
    """
    Returns the URL of a random site from your Supabase 'sites' table
    where can_jump = True. If none found, returns None.
    
    NOTE: This naive approach pulls ALL can_jump=True rows
    into Python, then picks randomly. If the table is large,
    you might want a more efficient approach or an RPC that
    picks one record on the server side.
    """
    # Fetch all rows where can_jump = True
    response = supabase.table("sites").select("*").eq("can_jump", True).execute()
    
    if not response.data:
        return None  # No sites found or error
    
    # Randomly pick one in Python
    random_entry = random.choice(response.data)
    
    # Adjust "source_url" below if your actual column name is different
    return random_entry.get("source_url")