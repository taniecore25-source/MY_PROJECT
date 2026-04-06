# MY_PROJECT

This repository contains a personal portfolio website with a Flask backend and a static frontend.

## Structure

- `backend/` - Flask server and backend files
  - `appp.py` - main Flask application
  - `indexx.html` - duplicate frontend copy inside backend folder
  - `requirementss.txt` - backend dependencies
- `fronend/` - frontend static website
  - `index.html` - portfolio HTML with contact form
- `requirements.txt` - Python dependencies for deployment
- `.gitignore` - ignored files for Git

## Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the backend:
   ```bash
   python backend/appp.py
   ```
4. Open the site in your browser:
   ```
   http://127.0.0.1:5000/
   ```

## Deployment on Render

- Build command: `pip install -r requirements.txt`
- Start command: `python backend/appp.py`
- Add `DATABASE_URL` as a Render environment variable

## Notes

- The backend serves the frontend from `fronend/index.html`.
- Do not commit `.env` or sensitive credentials to GitHub.
