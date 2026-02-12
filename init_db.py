import sqlite3
conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("SELECT role_id, jd_text FROM Role")
print("JD:", cur.fetchall())

cur.execute("SELECT candidate_id, skills FROM Candidate")
print("Candidate:", cur.fetchall())

conn.close()
