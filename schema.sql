CREATE TABLE Client (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    title TEXT,
    jd_text TEXT,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES Client(client_id)
);

CREATE TABLE Candidate (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    linkedin_url TEXT,
    skills TEXT,
    experience_years INTEGER
);

CREATE TABLE Application (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    role_id INTEGER,
    status TEXT,
    skill_match_percentage REAL,
    last_updated TEXT,
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id),
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
);
