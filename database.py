import sqlite3

# create sqlite db
def create_sqlite_db():  
    with sqlite3.connect('events_db.db') as conn:
        # Created 'event_table'
        conn.execute('''CREATE TABLE IF NOT EXISTS event_table
                        (timestamp TEXT, event_type TEXT, metric REAL)''')


# insert into db
def insert_sqlite_db(data):
    with sqlite3.connect('events_db.db') as conn:
        conn.execute("INSERT INTO event_table VALUES (?,?,?)", 
                     (data['timestamp'], data['event_type'], data['metric']))
    print(f"Event logged successfully: {data['timestamp']}")