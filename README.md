# AI Resume Analyzer

A polished Flask application that analyzes resumes against job descriptions using NLP-based skill extraction, keyword matching, and ATS-style scoring.

## What it does

- Accepts PDF and DOCX resume uploads
- Extracts resume text reliably with PyPDF2 and python-docx
- Cleans and preprocesses text using spaCy NLP
- Detects relevant skills through a curated keyword library
- Computes resume fit with cosine similarity and skill coverage
- Generates a professional score, matched skills, missing skills, and actionable suggestions

## Project structure

- `app.py` — Flask application entrypoint and web routes
- `templates/` — Jinja templates for page layout and results
- `static/` — Styling for an elegant interface
- `utils/text_utils.py` — text extraction, preprocessing, skill matching, and scoring logic
- `requirements.txt` — pinned Python dependencies

## Setup

1. Open PowerShell in the project folder:
   ```powershell
   cd "c:\Users\kunal\Desktop\AI analyser"
   ```
2. Create a virtual environment and activate it:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
4. Run the application:
   ```powershell
   .\venv\Scripts\python.exe app.py
   ```
   Or use the helper script:
   ```powershell
   .\run_app.bat
   ```
5. Open a browser and visit:
   ```text
   http://127.0.0.1:5000
   ```

## Additional notes

- If spaCy does not automatically install the language model, run:
  ```powershell
  .\venv\Scripts\python.exe -m spacy download en_core_web_sm
  ```
- For best results, use a resume with clear section headings and a complete job description.
- The app is designed to highlight where your resume can be improved for recruiter and ATS matching.
