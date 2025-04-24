@echo off
cd "C:\Users\callu\OneDrive\Documents\GitHub\AE-Attendances"
echo -------------------- >> log.txt
echo %DATE% %TIME% >> log.txt
"C:\Users\callu\AppData\Local\Programs\Python\Python311\python.exe" APIproject.py >> log.txt 2>&1