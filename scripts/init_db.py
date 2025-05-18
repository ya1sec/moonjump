import sqlite3
import csv
import os
import sys # Import the sys module

def init_db(csv_path: str = "arena_sites.csv", db_path: str = "sites.db") -> None:
    """Initialize the SQLite database from the CSV file."""
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the sites table
    cursor.execute("""
        CREATE TABLE sites (
            id INTEGER PRIMARY KEY,
            source_url TEXT,
            can_jump BOOLEAN,
            channel_name TEXT
        )
    """)
    
    # Import data from CSV
    csv.field_size_limit(sys.maxsize) # Increase the field size limit
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        processed_ids = set() # Keep track of processed IDs
        for row in reader:
            current_id = row['id']
            if current_id in processed_ids:
                print(f"Skipping duplicate ID: {current_id}")
                continue  # Skip if ID already processed
            processed_ids.add(current_id)

			# only add rows that have a source_url that starts with https://
            if not row['source_url'].startswith('https://'):
                print(f"Skipping row with non-https source_url: {row['source_url']}")
                continue
            
            cursor.execute(
                "INSERT INTO sites (id, source_url, can_jump, channel_name) VALUES (?, ?, ?, ?)",
                (row['id'], row['source_url'], True, row['channel_name'])
            )
    
    # Create an index on can_jump and source_url for faster queries
    cursor.execute("CREATE INDEX idx_jumpable_sites ON sites(can_jump, source_url)")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 