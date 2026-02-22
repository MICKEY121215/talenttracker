from flask import Flask, render_template, request, redirect, flash
import sqlite3
import pdfplumber
import os


app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

import re

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

SKILL_SET = {
    "python", "java", "sql", "flask", "django",
    "aws", "react", "javascript", "html",
    "css", "mongodb", "machine", "learning"
}

def extract_skills(text):
    import re
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = set(clean_text.split())

    found_skills = []

    for skill in SKILL_SET:
        if skill in clean_text:
            found_skills.append(skill)

    return ", ".join(sorted(found_skills))


def skill_match(jd_text, candidate_skills):

    stop_words = {
        "looking", "for", "and", "with", "developer", "engineer",
        "required", "experience", "in", "of", "a", "an", "the",
        "skills", "knowledge", "role", "position"
    }

    jd_words = re.sub(r'[^\w\s]', '', jd_text.lower()).split()
    cs_words = re.sub(r'[^\w\s]', '', candidate_skills.lower()).split()

    jd_set = set(word for word in jd_words if word not in stop_words)
    cs_set = set(cs_words)

    matched = jd_set & cs_set
    missing = jd_set - cs_set

    if len(jd_set) == 0:
        match_percent = 0.0
    else:
        match_percent = round((len(matched) / len(jd_set)) * 100, 2)

    return matched, missing, match_percent

@app.route("/dashboard")
def dashboard():
    db = get_db()
    cur = db.cursor()

    stats = cur.execute("""
        SELECT status, COUNT(*) 
        FROM Application 
        GROUP BY status
    """).fetchall()

    db.close()
    return render_template("dashboard.html", stats=stats)

@app.route("/")
def home():
    return redirect("/clients")

# -------- CLIENTS --------
@app.route("/clients", methods=["GET", "POST"])
def clients():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        name = request.form["name"].strip()
    try:
        cur.execute("INSERT INTO Client (name) VALUES (?)", (name,))
        db.commit()
        flash("Client added successfully.", "success")
    except sqlite3.IntegrityError:
        flash("Client already exists.", "error")

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

        client_id = request.form["client_id"]
        title = request.form["title"].strip()
        status = request.form["status"]

        jd_file = request.files.get("jd_file")

        jd_text = request.form.get("jd_text", "")
        save_path = None

        if jd_file and jd_file.filename != "":
            os.makedirs("uploads/jds", exist_ok=True)

            save_path = os.path.join("uploads/jds", jd_file.filename)
            jd_file.save(save_path)

            extracted_text = extract_text_from_pdf(save_path)
            jd_text = extract_skills(extracted_text)

        try:
            cur.execute("""
              INSERT INTO Role 
              (client_id, title, jd_text, jd_file_path, status)
            VALUES (?, ?, ?, ?, ?)
             """, (client_id, title, jd_text, save_path, status))
            db.commit()
            flash("Role added successfully.", "success")

        except sqlite3.IntegrityError:
            flash("This role already exists for the selected client.", "error")

    roles = cur.execute("""
        SELECT Role.role_id,
               Client.name,
               Role.title,
               Role.status,
               Role.jd_file_path
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

        name = request.form["name"].strip()
        linkedin = request.form["linkedin_url"].strip()
        experience = request.form["experience_years"]

        resume_file = request.files.get("resume")

        skills = request.form["skills"]
        save_path = None

        if resume_file and resume_file.filename != "":
            os.makedirs("uploads/resumes", exist_ok=True)

            save_path = os.path.join("uploads/resumes", resume_file.filename)
            resume_file.save(save_path)

            extracted_text = extract_text_from_pdf(save_path)
            skills = extract_skills(extracted_text)

        try:
            cur.execute("""
              INSERT INTO Candidate 
              (name, linkedin_url, skills, experience_years, resume_file_path)
              VALUES (?, ?, ?, ?, ?)
              """, (name, linkedin, skills, experience, save_path))
            db.commit()
            flash("Candidate added successfully.", "success")
        except sqlite3.IntegrityError:
            flash("Candidate already exists.", "error")

    candidates = cur.execute("SELECT * FROM Candidate").fetchall()

    db.close()
    return render_template("candidates.html", candidates=candidates)

@app.route("/delete_candidate/<int:candidate_id>")
def delete_candidate(candidate_id):
    db = get_db()
    cur = db.cursor()

    # Get resume file path
    cur.execute("SELECT resume_file_path FROM Candidate WHERE candidate_id = ?", (candidate_id,))
    result = cur.fetchone()

    # Delete resume file from disk
    if result and result[0]:
        import os
        if os.path.exists(result[0]):
            os.remove(result[0])

    # Delete related applications first (important)
    cur.execute("DELETE FROM Application WHERE candidate_id = ?", (candidate_id,))

    # Delete candidate
    cur.execute("DELETE FROM Candidate WHERE candidate_id = ?", (candidate_id,))

    db.commit()
    db.close()

    return redirect("/candidates")


# -------- APPLICATIONS --------
@app.route("/applications", methods=["GET", "POST"])
def applications():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        try:
            cur.execute("""
            INSERT INTO Application (candidate_id, role_id, status)
            VALUES (?, ?, ?)
            """, (
            request.form["candidate_id"],
            request.form["role_id"],
            request.form["status"]
            ))
            db.commit()
            flash("Application created successfully.", "success")

        except sqlite3.IntegrityError:
            flash("This candidate is already assigned to this role.", "error")


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

@app.route("/skill_match/<int:application_id>")
def skill_match_view(application_id):
    db = get_db()
    cur = db.cursor()

    app_data = cur.execute("""
        SELECT Role.jd_text, Candidate.skills
        FROM Application
        JOIN Role ON Application.role_id = Role.role_id
        JOIN Candidate ON Application.candidate_id = Candidate.candidate_id
        WHERE Application.application_id = ?
    """, (application_id,)).fetchone()

    matched, missing, percentage = skill_match(app_data[0], app_data[1])

    cur.execute("""
        UPDATE Application
        SET skill_match_percentage = ?
        WHERE application_id = ?
    """, (percentage, application_id))

    db.commit()
    db.close()

    return render_template(
        "skill_match.html",
        matched=matched,
        missing=missing,
        percentage=percentage
    )

# -------- UPDATE --------
@app.route("/update_status/<int:application_id>", methods=["POST"])
def update_status(application_id):
    new_status = request.form["status"]

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE Application
        SET status = ?
        WHERE application_id = ?
    """, (new_status, application_id))
    db.commit()
    db.close()

    return redirect("/applications")

# -------- RUN APP (ALWAYS LAST) --------
if __name__ == "__main__":
    app.run()
