@echo off
setlocal

REM ~~~~~~~
call updateGameFiles.bat
python updateImages.py
python updateDatabase.py --skip-prompts
python updateFilters.py --skip-prompts
python updateLangs.py

echo.
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo ~~~~~~~~~~~ ALL DONE ~~~~~~~~~~~~
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.
pause