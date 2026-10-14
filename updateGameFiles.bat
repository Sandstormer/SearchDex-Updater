@echo off
setlocal enabledelayedexpansion

REM ======= CONFIG =======
set "gameUrl=https://github.com/pagefaultgames/pokerogue.git"
set "gameSrcBranch=beta"
set "gameSrcDest=game_files"
set "gameDataBranch=game-data"
set "gameDataDest=game_files/data_output"
set "websiteUrl=https://github.com/Sandstormer/PokeRogue-Dex.git"
set "websiteDest=website"
echo.
REM ======= CLONE / UPDATE GAME FILES =======
if not exist "%gameSrcDest%" (
    REM If game folder doesn't exist, clone
    echo Cloning repository into %gameSrcDest%...
    if not "%gameSrcBranch%"=="" (
        git clone --depth 1 -b %gameSrcBranch% --shallow-submodules --recursive %gameUrl% %gameSrcDest%
    ) else (
        git clone --depth 1 %gameUrl% %gameSrcDest%
    )
) else (
    if not exist "%gameSrcDest%\.git" (
        REM If game folder exists but is NOT a git repo
        echo Folder exists at %gameSrcDest% but is not a git repository. Delete it manually to continue.
        pause
        exit
    ) else (
        REM If game folder repo exists, update it
        echo Resetting repository at %gameSrcDest%...
        git -C "%gameSrcDest%" fetch --depth 1 origin
        if not "%gameSrcBranch%"=="" (
            git -C "%gameSrcDest%" fetch --depth 1 origin %gameSrcBranch%
            git -C "%gameSrcDest%" checkout -B %gameSrcBranch% FETCH_HEAD
        ) else (
            git -C "%gameSrcDest%" reset --hard origin/HEAD
        )
        git -C "%gameSrcDest%" clean -fdx
        git -C "%gameSrcDest%" submodule update --init --recursive --force --depth 1
    )
)
echo.
REM ======= CLONE WEBSITE (DOES NOT OVERWRITE) =======
REM If folder doesn't exist, clone
if exist "%websiteDest%" (
    echo SearchDex website folder already exists, so won't be updated...
) else (
    echo Cloning SearchDex website files into %websiteDest%...
    git clone --depth 1 %websiteUrl% %websiteDest%
)
echo.
REM ======= CLONE FROM GAME DATA BRANCH =======
if not exist "%gameDataDest%" (
    REM If data export folder doesn't exist, clone
    echo Cloning data export files into %gameDataDest%...
    git clone --depth 1 -b %gameDataBranch% %gameUrl% %gameDataDest%
) else (
    REM If data export folder repo exists, update it
    echo Updating export files in %gameDataDest%...
    git -C "%gameDataDest%" fetch --depth 1 origin %gameDataBranch%
    git -C "%gameDataDest%" checkout -B %gameDataBranch% FETCH_HEAD
    git -C "%gameDataDest%" clean -fdx
)
REM Copy exported data from the selected branch into its own folder
REM This is so you don't have to specify the branch again in updateDatabase.py
robocopy "%gameDataDest%\%gameSrcBranch%" "%gameDataDest%\selected" /E
echo.
echo ======= END OF updateGameFiles.bat =======
echo.