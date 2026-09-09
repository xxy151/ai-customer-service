@echo off
title AI Customer Service Web
cd /d "%~dp0"
echo Starting AI customer service ...  http://localhost:8501
.venv\Scripts\python.exe -m streamlit run app.py --server.port 8501
pause
