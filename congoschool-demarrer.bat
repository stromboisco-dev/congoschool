@echo off
title CongoSchool - Demarrage
color 0B
echo ============================================
echo    CONGOSCHOOL - DEMARRAGE
echo ============================================
echo.
echo Ouverture de CongoSchool...
echo.
echo Ordinateur : http://localhost:5000
echo Telephone  : http://localhost:5000
echo.

cd /d "%~dp0"
python app.py

pause
