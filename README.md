# Secure User Authentication System

A web-based user authentication system built using Python, Flask, SQLite, and Flask-Bcrypt.

## Features

* User registration and login
* Password hashing using Flask-Bcrypt
* Password validation
* Email validation
* Duplicate email prevention
* Session-based authentication
* Protected dashboard
* Logout functionality
* CSRF protection using Flask-WTF
* Parameterized SQL queries to help prevent SQL injection
* HTTP-only session cookies

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Password Hashing:** Flask-Bcrypt
* **CSRF Protection:** Flask-WTF
* **Frontend:** HTML, CSS, JavaScript

## Project Structure

```text
auth-system/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   ├── signup.html
│   ├── login.html
│   └── dashboard.html
└── static/
    └── style.css
```

## Requirements

* Python 3
* pip
* A web browser

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd auth-system
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the secret key

In Windows PowerShell, run:

```powershell
$env:FLASK_SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
```

This generates a secret key for the current terminal session.

Generate a new key whenever you start a new terminal session. Existing login sessions may become invalid when the key changes.

### 6. Run the application

```bash
python app.py
```

Open the local address displayed in the terminal, usually:

```text
http://127.0.0.1:5000
```

## Application Routes

| Method | Endpoint     | Description                      |
| ------ | ------------ | -------------------------------- |
| GET    | `/`          | Displays the registration page   |
| POST   | `/register`  | Registers a new user             |
| GET    | `/login`     | Displays the login page          |
| POST   | `/login`     | Authenticates a user             |
| GET    | `/dashboard` | Displays the protected dashboard |
| POST   | `/logout`    | Logs out the current user        |

## Security Checklist

* [x] Passwords are hashed before being stored.
* [x] Parameterized SQL queries are used for database operations.
* [x] Password validation is implemented.
* [x] Duplicate email registration is handled.
* [x] Session-based authentication is implemented.
* [x] The dashboard checks whether a user is logged in.
* [x] CSRF protection is configured using Flask-WTF.
* [x] HTTP-only session cookies are configured.
* [ ] Verify that untrusted content is safely escaped to prevent XSS.
* [ ] Verify that requests without valid CSRF tokens are rejected.
* [ ] Verify production cookie settings and HTTPS configuration.

**Note:** The unchecked items must be tested and confirmed before marking them complete.

## Environment Configuration

The `.env.example` file provides a placeholder for the Flask secret key.

Do not upload actual secret keys, passwords, or other credentials to GitHub.

The application currently reads `FLASK_SECRET_KEY` from the environment. The commands above set it directly in the terminal.

## Database

The application uses SQLite. The database file is created locally by the application when database initialization runs.

The local database file should not be committed to the repository.

## Limitations

This project is intended as a learning project. Review the security configuration and test all authentication flows before deploying it publicly.

## Author

Developed as a user authentication system project.
