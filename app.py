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

# -------- ROLES --------
@app.route("/roles", methods=["GET", "POST"])
def roles():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        client_id = request.form["client_id"]
        title = request.form["title"]
        jd_text = request.form["jd_text"]
        status = request.form["status"]

        cur.execute("""
            INSERT INTO Role (client_id, title, jd_text, status)
            VALUES (?, ?, ?, ?)
        """, (client_id, title, jd_text, status))
        db.commit()

    roles = cur.execute("""
        SELECT Role.role_id, Client.name, Role.title, Role.status
        FROM Role
        JOIN Client ON Role.client_id = Client.client_id
    """).fetchall()

    clients = cur.execute("SELECT * FROM Client").fetchall()
    db.close()

    return render_template("roles.html", roles=roles, clients=clients)

if __name__ == "__main__":
    app.run(debug=True)
