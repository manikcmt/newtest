# Simple FastAPI + MySQL CRUD (with Age, without PATCH)

A beginner project with **Name**, **Email** and **Age**. The webpage has **Add**, **Edit** and **Delete** buttons. There is NO separate age update button and NO PATCH endpoint.

## Project files

- `main.py`: FastAPI application and HTML page; adds a missing age column to older databases
- `database.py`: MySQL database connection
- `models.py`: user table with id, name, email and age
- `schemas.py`: validates name, email and age (0–120)
- `routers.py`: GET, POST, PUT and DELETE (no PATCH)
- `static/index.html`: beginner HTML form and table
- `static/styles.css`: basic CSS
- `static/app.js`: simple JavaScript fetch API
- `.env.example`: example database credentials
- `setup.sql`: SQL to create database
- `requirements.txt`: Python dependencies

## Run on Windows

1. Extract the ZIP; open the `fastapi_mysql_crud` folder (containing `main.py`) in VS Code.
2. Start MySQL. In MySQL Workbench, execute `setup.sql` to create the `crud_db` database.
3. In the VS Code PowerShell terminal run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

4. Open http://127.0.0.1:8000/ (frontend) or http://127.0.0.1:8000/docs (Swagger).

`.env.example` contains `root` / `root`, matching your local database setup. Don't publish `.env` or use root credentials in production.

## Add, Edit, and Delete

- **Add User**: provide Name, Email and Age, then click Add User. Uses `POST /users/`.
- **Edit User**: click Edit in a table row, change Name, Email **or Age** in the form, then click Update User. Uses `PUT /users/{user_id}` with all three fields.
- **Delete User**: click Delete and confirm. Uses `DELETE /users/{user_id}`.
- **List Users**: uses `GET /users/`. There is no PATCH endpoint.

## Existing database warning

This version **never drops the age column**. If the table already has an age column, current ages are preserved. If you ran the earlier Name+Email-only project and its startup already removed the column, those former ages cannot be automatically recovered from this project; restore them from a database backup if available. This version re-adds a missing age column with a default value of `0` for existing users, which you can change using Edit (PUT).

If you still see the old page, restart the server and refresh with Ctrl + F5. Run the webpage through FastAPI, not by double-clicking the HTML file.
