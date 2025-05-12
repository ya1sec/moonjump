import random
import os
import sqlite3
from typing import Optional

def get_random_jumpable_site(db_path: str = "sites.db") -> Optional[str]:
    """Returns a random site from the database where can_jump=True and source_url starts with 'https'."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get the total count of jumpable sites
        cursor.execute("""
            SELECT COUNT(*) 
            FROM sites 
            WHERE can_jump = 1 
            AND source_url LIKE 'https%'
        """)
        total_records = cursor.fetchone()[0]
        
        if total_records == 0:
            print("No jumpable sites found")
            return None
            
        # Pick a random offset
        offset = random.randint(0, total_records - 1)
        
        # Get a random site
        cursor.execute("""
            SELECT source_url 
            FROM sites 
            WHERE can_jump = 1 
            AND source_url LIKE 'https%'
            LIMIT 1 
            OFFSET ?
        """, (offset,))
        
        result = cursor.fetchone()
        if result:
            site_url = result[0]
            print(f"Selected site: {site_url}")
            return site_url
            
    except Exception as e:
        print(f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()
        
    return None 

def get_random_jumpable_site_wrapper():
    """Wrapper function to maintain compatibility with existing code."""
    return get_random_jumpable_site()