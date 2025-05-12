import sqlite3
import csv
import os

def init_db(csv_path: str = "arena_sites_checked.csv", db_path: str = "sites.db") -> None:
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
            jump_block_reason TEXT
        )
    """)
    
    # Import data from CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                "INSERT INTO sites (id, source_url, can_jump, jump_block_reason) VALUES (?, ?, ?, ?)",
                (row['id'], row['source_url'], row['can_jump'] == 'True', row['jump_block_reason'])
            )
    
    # Create an index on can_jump and source_url for faster queries
    cursor.execute("CREATE INDEX idx_jumpable_sites ON sites(can_jump, source_url)")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 