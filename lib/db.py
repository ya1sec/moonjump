import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# the env file is in the root directory
load_dotenv(dotenv_path="../.env")

# SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
SUPABASE_URL="https://milovxdtnbgxocmomoxs.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1pbG92eGR0bmJneG9jbW9tb3hzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxMjAyNzMsImV4cCI6MjA1MzY5NjI3M30.0RHwFUfdd2YNJRsitt8UAhtN-ExfLBXXzxO9LGaR944"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_random_jumpable_site():
    """Returns a random site from 'sites' where can_jump=True."""

    # Known total records
    TOTAL_RECORDS = 2331

    # 1) Pick a random offset
    offset = random.randint(0, TOTAL_RECORDS - 1)
    print(f"Selected random offset: {offset}")

    # 2) Fetch exactly one row at that offset
    try:
        row_response = (
            supabase.table("sites")
            .select("id, source_url, can_jump")  # Fetch important fields
            .eq("can_jump", True)
            .range(offset, offset)  # Fetch exactly one row
            .execute()
        )

        print(f"Query response: {row_response}")

        if row_response.data and len(row_response.data) > 0:
            site_url = row_response.data[0].get("source_url")
            print(f"Selected site: {site_url}")
            return site_url
        else:
            print("No data returned from query.")

    except Exception as e:
        print(f"Query error: {e}")

    return None

# def get_random_jumpable_site():
#     """
#     Returns the URL of a random site from your Supabase 'sites' table
#     where can_jump = True. If none found, returns None.
    
#     NOTE: This naive approach pulls ALL can_jump=True rows
#     into Python, then picks randomly. If the table is large,
#     you might want a more efficient approach or an RPC that
#     picks one record on the server side.
#     """
#     # Fetch all rows where can_jump = True
#     # response = supabase.table("sites").select("*").eq("can_jump", True).execute()

# 	# May work but can be slow on large tables
#     response = supabase.table("sites").select("source_url") \
# 		.eq("can_jump", True) \
# 		.order("random()") \
# 		.limit(1) \
# 		.execute()
    
#     if not response.data:
#         return None  # No sites found or error
    
#     # Randomly pick one in Python
#     random_entry = random.choice(response.data)
    
#     # Adjust "source_url" below if your actual column name is different
#     return random_entry.get("source_url")