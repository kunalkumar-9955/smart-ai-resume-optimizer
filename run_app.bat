@echo off
cd /d "%~dp0"
if exist venv\Scripts\python.exe (
    call venv\Scripts\python.exe app.py
) else (
    echo Virtual environment not found. Run: python -m venv venv
)
