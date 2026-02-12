import sqlite3
conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("SELECT role_id, jd_text FROM Role")
print(cur.fetchall())

cur.execute("SELECT candidate_id, skills FROM Candidate")
print(cur.fetchall())

conn.close()
