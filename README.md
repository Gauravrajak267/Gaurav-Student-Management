# Student Record Management API

A full-stack Student Management System featuring a RESTful backend API built with FastAPI and SQLAlchemy, paired with an interactive web frontend served as static assets.

---

## Project Structure

student-management/
├── static/
│   └── index.html      # Frontend HTML/CSS/JS UI
├── main.py             # FastAPI backend application & DB models
├── requirements.txt    # Project Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # Project documentation

---

## Prerequisites

Ensure you have the following installed on your system:

* Python 3.10+
* pip (Python package manager)
* Git

---

## Installation & Setup

1. Clone the repository:
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd student-management
2. Create and activate a virtual environment:
* Windows (PowerShell):
python -m venv .venv
..venv\Scripts\Activate.ps1
* Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate


3. Install dependencies:
pip install -r requirements.txt

---

## Running the Application

Start the FastAPI application by executing main.py:

python main.py

The server will start locally at: [http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)

---

## Testing the Application

1. Interactive Web Frontend
Access the user interface directly in your browser:

* Frontend UI: [http://127.0.0.1:8000/frontend/](https://www.google.com/search?q=http://127.0.0.1:8000/frontend/)

2. Interactive Swagger API Docs
FastAPI provides automatic interactive documentation to test all endpoints:

* Swagger UI: [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

---

## API Endpoints Overview

* GET / : API status check (Status: 200 OK)
* GET /students : Retrieve all student records (Status: 200 OK)
* POST /students : Create a new student record (Status: 201 Created)
* GET /students/{student_id} : Retrieve a specific student by ID (Status: 200 OK)
* PATCH /students/{student_id} : Update a student's information by ID (Status: 200 OK)
* DELETE /students/{student_id} : Delete a student record by ID (Status: 204 No Content)

---

## Security & Data Privacy

No passwords, API keys, secrets, or real personally identifiable information (PII) are included in this project repository. Database files (.db) and virtual environments (.venv) are ignored via .gitignore.