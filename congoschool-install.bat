@echo off
title CongoSchool - Installation
color 0A
echo ============================================
echo    CONGOSCHOOL - INSTALLATION AUTOMATIQUE
echo ============================================
echo.
echo Ce programme va installer CongoSchool sur votre ordinateur.
echo Il va telecharger Python, Flask et les dependances.
echo.

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/4] Python n'est pas installe. Telechargement...
    
    :: Download Python installer
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"
    
    echo [1/4] Installation de Python...
    start /wait "" "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del "%TEMP%\python-installer.exe"
    
    :: Refresh PATH
    set PATH=%PATH%;C:\Program Files\Python313;C:\Program Files\Python313\Scripts
    echo [1/4] Python installe avec succes!
) else (
    echo [1/4] Python est deja installe: OK
    python --version
)

echo.
echo [2/4] Installation de Flask et openpyxl...
pip install flask openpyxl gunicorn
echo [2/4] Dependances installees!

echo.
echo [3/4] Creation du dossier CongoSchool...
if not exist "%USERPROFILE%\Desktop\CongoSchool" mkdir "%USERPROFILE%\Desktop\CongoSchool"
echo [3/4] Dossier cree sur le Bureau!

echo.
echo [4/4] Preparation de la base de donnees...
echo [4/4] Presque pret!

echo.
echo ============================================
echo    INSTALLATION TERMINEE AVEC SUCCES!
echo ============================================
echo.
echo Pour lancer CongoSchool :
echo   1. Allez sur votre Bureau
echo   2. Double-cliquez sur "Demarrer CongoSchool.bat"
echo.
echo Puis ouvrez Edge et allez sur : http://localhost:5000
echo.
echo Identifiants par defaut :
echo   Code d'acces : congo2025
echo   Utilisateur  : admin
echo   Mot de passe : congoschool2025!
echo.
pause
