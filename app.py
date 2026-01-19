from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return redirect("/clients")

# -------- CLIENTS --------
@app.route("/clients", methods=["GET", "POST"])
def clients():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        name = request.form["name"]
        cur.execute("INSERT INTO Client (name) VALUES (?)", (name,))
        db.commit()

    clients = cur.execute("SELECT * FROM Client").fetchall()
    db.close()
    return render_template("clients.html", clients=clients)

@app.route("/delete_client/<int:client_id>")
def delete_client(client_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM Role WHERE client_id = ?", (client_id,))
    cur.execute("DELETE FROM Client WHERE client_id = ?", (client_id,))
    db.commit()
    db.close()
    return redirect("/clients")

# -------- ROLES --------
@app.route("/roles", methods=["GET", "POST"])
def roles():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        cur.execute("""
            INSERT INTO Role (client_id, title, jd_text, status)
            VALUES (?, ?, ?, ?)
        """, (
            request.form["client_id"],
            request.form["title"],
            request.form["jd_text"],
            request.form["status"]
        ))
        db.commit()

    roles = cur.execute("""
        SELECT Role.role_id, Client.name, Role.title, Role.status
        FROM Role
        JOIN Client ON Role.client_id = Client.client_id
    """).fetchall()

    clients = cur.execute("SELECT * FROM Client").fetchall()
    db.close()
    return render_template("roles.html", roles=roles, clients=clients)

@app.route("/delete_role/<int:role_id>")
def delete_role(role_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM Role WHERE role_id = ?", (role_id,))
    db.commit()
    db.close()
    return redirect("/roles")

# -------- CANDIDATES --------
@app.route("/candidates", methods=["GET", "POST"])
def candidates():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        cur.execute("""
            INSERT INTO Candidate (name, linkedin_url, skills, experience_years)
            VALUES (?, ?, ?, ?)
        """, (
            request.form["name"],
            request.form["linkedin_url"],
            request.form["skills"],
            request.form["experience_years"]
        ))
        db.commit()

    candidates = cur.execute("SELECT * FROM Candidate").fetchall()
    db.close()
    return render_template("candidates.html", candidates=candidates)

# -------- APPLICATIONS --------
@app.route("/applications", methods=["GET", "POST"])
def applications():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        cur.execute("""
            INSERT INTO Application (candidate_id, role_id, status)
            VALUES (?, ?, ?)
        """, (
            request.form["candidate_id"],
            request.form["role_id"],
            request.form["status"]
        ))
        db.commit()

    applications = cur.execute("""
        SELECT Application.application_id,
               Candidate.name,
               Role.title,
               Application.status
        FROM Application
        JOIN Candidate ON Application.candidate_id = Candidate.candidate_id
        JOIN Role ON Application.role_id = Role.role_id
    """).fetchall()

    candidates = cur.execute("SELECT * FROM Candidate").fetchall()
    roles = cur.execute("SELECT * FROM Role").fetchall()

    db.close()
    return render_template(
        "applications.html",
        applications=applications,
        candidates=candidates,
        roles=roles
    )

# -------- RUN APP (ALWAYS LAST) --------
if __name__ == "__main__":
    app.run(debug=True)
