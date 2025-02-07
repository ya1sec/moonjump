import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv

def get_random_jumpable_site(supabase_client):
    """Returns a random site from 'sites' where can_jump=True and source_url starts with 'https'."""

    # 1) Fetch the count of records where source_url starts with 'https'
    # count_response = (
    #     supabase_client.table("sites")
    #     .select("id")  # Selecting id to count records
    #     .ilike("source_url", "https%")  # Filter for source_url starting with 'https'
    #     .execute()
    # )

    # TOTAL_RECORDS = len(count_response.data)  # Set total records based on count
    # print(f"Total records with 'https': {TOTAL_RECORDS}")

    # # 2) Pick a random offset
    # if TOTAL_RECORDS == 0:
    #     print("No records found with 'https'.")
    #     return None

    TOTAL_RECORDS = 1000

    offset = random.randint(0, TOTAL_RECORDS - 1)
    print(f"Selected random offset: {offset}")

    # 3) Fetch exactly one row at that offset
    try:
        row_response = (
            supabase_client.table("sites")
            .select("id, source_url")  # Fetch important fields
            .ilike("source_url", "https%")  # Filter for source_url starting with 'https'
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