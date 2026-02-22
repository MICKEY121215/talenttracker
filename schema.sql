CREATE TABLE Client (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    title TEXT,
    jd_text TEXT,
    jd_file_path TEXT,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    UNIQUE(client_id, title)
);

CREATE TABLE Candidate (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    linkedin_url TEXT,
    skills TEXT,
    experience_years INTEGER,
    resume_file_path TEXT,
    UNIQUE(name, linkedin_url)
);

CREATE TABLE Application (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    role_id INTEGER,
    status TEXT,
    UNIQUE(candidate_id, role_id)
);
