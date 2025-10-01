# FastAPI + Svelte full-stack tutorial

This repository demonstrates a minimal full-stack application that combines a FastAPI backend with a Svelte (Vite) frontend. It showcases common features such as authentication with JWT, a SQL database (SQLite) managed through SQLAlchemy, and a fully reactive CRUD interface.

## Project structure

```
.
├── backend
│   ├── app
│   │   ├── auth.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── package.json
│   ├── src
│   │   ├── App.svelte
│   │   ├── app.css
│   │   ├── lib
│   │   │   └── api.js
│   │   ├── main.js
│   │   └── stores
│   │       └── auth.js
│   ├── svelte.config.js
│   ├── tsconfig.base.json
│   ├── tsconfig.json
│   └── vite.config.js
└── README.md
```

## Backend

The backend exposes:

- **Authentication** using username/password with hashed storage and JWT access tokens.
- **User profile** endpoint to return the authenticated user's data.
- **Item CRUD** endpoints backed by SQLite and SQLAlchemy.

### Install & run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## Frontend

The Svelte frontend contains registration/login forms, displays the authenticated user's profile, and allows creating, updating, and deleting personal items. It communicates with the backend through a small Axios client and stores the JWT token in `localStorage`.

### Install & run

```bash
cd frontend
npm install
npm run dev
```

By default Vite runs on `http://127.0.0.1:5173`. A development proxy forwards `/api` requests to the FastAPI server running on `http://localhost:8000`.

## Demo workflow

1. Start the backend with Uvicorn.
2. Start the frontend with `npm run dev`.
3. Register a new account in the UI, then sign in.
4. Create, edit, and delete items. All operations require authentication and persist in the SQLite database (`backend/app.db`).

## Testing the API manually

```bash
# Register
http POST :8000/auth/register email=user@example.com password=secret123

# Login to get an access token
http --form POST :8000/auth/token username=user@example.com password=secret123

# Use the token for authenticated requests
http GET :8000/items "Authorization:Bearer <token>"
```

Replace the HTTPie commands with `curl` if you prefer.
