import random
import os
import sqlite3
from typing import Optional
import contextlib
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Module-level cache for the count of jumpable https sites.
# -1 indicates the cache is stale and needs to be refreshed.
_cached_jumpable_sites_count: int = -1

@contextlib.contextmanager
def get_db_cursor(db_path: str = "sites.db"):
    """Context manager for SQLite database connections."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn.cursor()
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        if conn:
            conn.rollback() # Rollback changes on error
        raise # Re-raise the exception to be handled by the caller if necessary
    finally:
        if conn:
            conn.close()

def init_db(db_path: str = "sites.db"):
    """Initializes the database and creates the 'sites' table if it doesn't exist."""
    global _cached_jumpable_sites_count
    try:
        with get_db_cursor(db_path) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT UNIQUE NOT NULL,
                    can_jump INTEGER DEFAULT 1,
                    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    info TEXT
                )
            """)
        logging.info(f"Database initialized and 'sites' table ensured at {db_path}")
        _cached_jumpable_sites_count = -1 # Invalidate cache after DB init
    except sqlite3.Error as e:
        # Context manager already logged the error
        # If specific additional handling/logging for init_db failure is needed, add here
        pass

def get_random_jumpable_site(db_path: str = "sites.db") -> Optional[str]:
    """Returns a random site from the database where can_jump=True and source_url starts with 'https'. Uses a cache for the total count."""
    global _cached_jumpable_sites_count
    try:
        with get_db_cursor(db_path) as cursor:
            current_count = _cached_jumpable_sites_count
            
            if current_count == -1:
                # Cache is stale, refresh it
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM sites 
                    WHERE can_jump = 1 
                    AND source_url LIKE 'https%'
                """)
                count_result = cursor.fetchone()
                if not count_result: # Should ideally not happen with COUNT(*)
                    logging.error("Failed to fetch count of jumpable sites.")
                    _cached_jumpable_sites_count = -1 # Keep cache stale
                    return None
                current_count = count_result[0]
                _cached_jumpable_sites_count = current_count
                logging.info(f"Refreshed jumpable sites count: {current_count}")
            
            if current_count == 0:
                logging.info("No jumpable sites found (cached or fresh count is 0).")
                return None
                
            # Pick a random offset
            # Ensure current_count is positive before calling randint to avoid ValueError for randint(0, -1)
            offset = random.randint(0, current_count - 1)
            
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
                logging.info(f"Selected site: {site_url} (count used: {current_count}, offset: {offset})")
                return site_url
            else:
                # This can happen if the cache was positive but items were removed
                # (e.g., by another process or a concurrent request that marked a site non-jumpable).
                # Invalidate the cache so it's refreshed on the next call.
                logging.warning(f"Cache inconsistency: Count was {current_count}, but no site found at offset {offset}. Invalidating cache.")
                _cached_jumpable_sites_count = -1 
                return None

    except sqlite3.Error:
        # Context manager already logged the error.
        # Invalidate cache on any DB error during this process to be safe.
        _cached_jumpable_sites_count = -1
        pass # Current behavior is to return None on error
        
    return None 

def mark_site_as_not_jumpable(site_url: str, db_path: str = "sites.db") -> None:
    """Marks a site as not jumpable and invalidates the jumpable sites count cache if necessary."""
    global _cached_jumpable_sites_count
    logging.info(f"Attempting to mark site as not jumpable: {site_url}")
    try:
        with get_db_cursor(db_path) as cursor:
            # Check if the site was jumpable and would have been part of the cached count
            was_potentially_in_cache = False
            if site_url.startswith('https://'):
                cursor.execute("SELECT can_jump FROM sites WHERE source_url = ?", (site_url,))
                current_site_status = cursor.fetchone()
                if current_site_status and current_site_status[0] == 1:
                    was_potentially_in_cache = True
            
            cursor.execute("UPDATE sites SET can_jump = 0 WHERE source_url = ?", (site_url,))
            
            if was_potentially_in_cache:
                logging.info(f"Site {site_url} marked non-jumpable. Invalidating jumpable sites count cache.")
                _cached_jumpable_sites_count = -1
                
    except sqlite3.Error:
        # Context manager already logged the error.
        # Consider invalidating cache here too, though subsequent get calls will likely catch inconsistencies.
        # For now, rely on get_random_jumpable_site's invalidation logic.
        print(f"Error marking site as not jumpable (specific): {e}") # This 'e' is not defined, remove or fix. Will remove.
        pass