@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
".venv\Scripts\python.exe" -m streamlit run basic_app.py --server.port 8502
) else (
"..\.venv\Scripts\python.exe" -m streamlit run basic_app.py --server.port 8502
)
pause
