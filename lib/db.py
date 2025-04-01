import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv

def get_random_jumpable_site(supabase_client):
    """Returns a random site from 'sites' where can_jump=True and source_url starts with 'https'."""
    
    # Validate Supabase client
    if not supabase_client or not hasattr(supabase_client, 'table'):
        print("Error: Invalid Supabase client")
        return None
        
    try:
        # First try to get the total count of records
        count_response = (
            supabase_client.table("sites")
            .select("id", count="exact")
            .ilike("source_url", "https%")
            .execute()
        )
        
        if not count_response or not count_response.count:
            print("Error: Could not get record count")
            return None
            
        total_records = count_response.count
        
        if total_records == 0:
            print("No records found with 'https'")
            return None
            
        # Pick a random offset
        offset = random.randint(0, total_records - 1)
        print(f"Selected random offset: {offset}")

        # Fetch one row at that offset
        row_response = (
            supabase_client.table("sites")
            .select("source_url")
            .ilike("source_url", "https%")
            .range(offset, offset)
            .limit(1)
            .execute()
        )

        if row_response and row_response.data and len(row_response.data) > 0:
            site_url = row_response.data[0].get("source_url")
            if site_url and site_url.startswith("https"):
                print(f"Selected site: {site_url}")
                return site_url
            else:
                print("Invalid URL format in response")
        else:
            print("No data returned from query")

    except Exception as e:
        print(f"Supabase query error: {str(e)}")
        
    return None