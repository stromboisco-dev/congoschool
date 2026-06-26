@echo off
chcp 65001 >nul
title CongoSchool - Serveur
echo.
echo   CongoSchool - Gestion Scolaire
echo   =============================
echo.
cd /d "%~dp0"
python app.py
pause
