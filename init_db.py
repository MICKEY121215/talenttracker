import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Client (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT COLLATE NOCASE UNIQUE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    title TEXT COLLATE NOCASE,
    jd_text TEXT,
    jd_file_path TEXT,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    UNIQUE(client_id, title)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Candidate (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT COLLATE NOCASE,
    linkedin_url TEXT COLLATE NOCASE,
    skills TEXT,
    experience_years INTEGER,
    resume_file_path TEXT,
    UNIQUE(name, linkedin_url)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Application (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    role_id INTEGER,
    status TEXT,
    UNIQUE(candidate_id, role_id)
);
""")

conn.commit()
conn.close()

print("Database created successfully")