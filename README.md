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

---

## Folder Structure
