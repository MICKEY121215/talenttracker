# TalentTracker – Week 1

## Project Overview
TalentTracker is a simple Applicant Tracking System (ATS) built using Flask and SQLite.  
The goal of Week 1 is to understand the recruitment flow and build the foundation of the system.

This is an internal HR tool and not a public-facing application.

---

## Week 1 Objectives
- Understand basic recruitment workflow
- Design database schema
- Build a Flask application
- Implement Client Management
- Implement Role / Job Description Management
- Store and retrieve data using SQLite

---

## Recruitment Flow (Week 1 Scope)
1. **Client** – Company for which hiring is done  
2. **Role / Job Description** – Job opening under a client  

( Candidate and Application tracking will be implemented in later weeks )

---

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS (basic, no frameworks)

---

## Features Implemented in Week 1

### 1. Client Management
- Add a new client
- View list of all clients
- Data stored in SQLite database

### 2. Role / Job Description Management
- Add job roles under a client
- Store job description text
- Mark role status as Open or Closed
- View all roles with corresponding client name

---

## Database Schema (Week 1)

### Client Table
- client_id (Primary Key)
- name

### Role Table
- role_id (Primary Key)
- client_id (Foreign Key)
- title
- jd_text
- status

# TalentTracker – Week 2

## Project Overview
TalentTracker is a simple Applicant Tracking System (ATS) built using Flask and SQLite.
Week 2 focuses on implementing the **core ATS functionality** by adding candidates and
tracking applications between candidates and job roles.

This system simulates a real recruitment workflow used by HR teams.

---

## Week 2 Objectives
- Implement Candidate Management
- Implement Application Tracking (ATS Core)
- Map candidates to job roles
- Track recruitment status
- Use relational database joins
- Extend the Flask application cleanly

---

## Recruitment Flow (Week 2 Scope)

Client → Role → Candidate → Application

- A client can have multiple roles
- A candidate can apply to multiple roles
- Each application has a recruitment status

---

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS (basic, no frameworks)

---

## Features Implemented in Week 2

### 1. Candidate Management
- Add candidate profile
- Store LinkedIn URL, skills, and experience
- View list of all candidates

### 2. Application Tracking (Core ATS)
- Assign a candidate to a job role
- Track recruitment status
- One candidate can apply to multiple roles
- View applications with candidate name and role title

### 3. Status Tracking
Supported recruitment statuses:
- Sourced
- Contacted
- Interviewing
- Offered
- Rejected

---

## Database Schema (Week 2)

### Candidate Table
- candidate_id (Primary Key)
- name
- linkedin_url
- skills
- experience_years

### Application Table
- application_id (Primary Key)
- candidate_id (Foreign Key)
- role_id (Foreign Key)
- status
- skill_match_percentage (to be used in Week 3)
- last_updated

