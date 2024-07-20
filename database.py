import sqlite3

# Function to create a SQLite connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create the schedule table
def create_table(conn):
    sql_create_schedule_table = """
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_name TEXT NOT NULL,
        time INTEGER NOT NULL,
        difficulty TEXT NOT NULL,
        break_time INTEGER NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_schedule_table)
    except sqlite3.Error as e:
        print(e)

# Function to insert a new activity into the schedule table
def insert_activity(conn, activity_name, time, difficulty, break_time):
    sql = """
    INSERT INTO schedule (activity_name, time, difficulty, break_time)
    VALUES (?, ?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, (activity_name, time, difficulty, break_time))
    conn.commit()
    return cur.lastrowid

# Function to retrieve all activities from the schedule table
def fetch_activities(conn):
    cur = conn.cursor()
    cur.execute("SELECT activity_name, time, difficulty, break_time FROM schedule")
    rows = cur.fetchall()
    return rows

# Main function to test the database operations
def main():
    database = r"day_planner.db"  # Path to your SQLite database file
    conn = create_connection(database)
    if conn is not None:
        # Create schedule table
        create_table(conn)

        # Example: Insert activity
        insert_activity(conn, "Study", 60, "m", 10)

        # Example: Fetch all activities
        activities = fetch_activities(conn)
        for activity in activities:
            print(activity)

        conn.close()
    else:
        print("Error! cannot create database connection.")

if __name__ == '__main__':
    main()
