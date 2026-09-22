@echo off
setlocal enabledelayedexpansion

REM ======= CONFIG =======
set "gameUrl=https://github.com/pagefaultgames/pokerogue.git"
set "gameBranch=main"
set "gameDest=game_files"

set "websiteUrl=https://github.com/Sandstormer/PokeRogue-Dex.git"
set "websiteDest=website"

REM ======= CLONE / UPDATE GAME FILES =======
del "game_files/node_modules" /Q
echo Processing %gameDest%

if not exist "%gameDest%" (
    REM If game folder doesn't exist, clone
    echo Cloning repository into %gameDest%...
    if not "%gameBranch%"=="" (
        git clone --depth 1 -b %gameBranch% --shallow-submodules --recursive %gameUrl% %gameDest%
    ) else (
        git clone --depth 1 %gameUrl% %gameDest%
    )
) else (
    if not exist "%gameDest%\.git" (
        REM If game folder exists but is NOT a git repo
        echo Folder exists at %gameDest% but is not a git repository.
        echo Delete it manually to continue.
        pause
        exit /b 1
    ) else (
        REM If game folder repo exists, update it
        echo Resetting repository at %gameDest%...
        git -C "%gameDest%" fetch --depth 1 origin
        if not "%gameBranch%"=="" (
            git -C "%gameDest%" fetch --depth 1 origin %gameBranch%
            git -C "%gameDest%" checkout -B %gameBranch% FETCH_HEAD
        ) else (
            git -C "%gameDest%" reset --hard origin/HEAD
        )
        git -C "%gameDest%" clean -fdx 
        git -C "%gameDest%" submodule update --init --recursive --force --depth 1
    )
)

REM ======= CLONE WEBSITE (ONLY ONCE) =======
REM If folder doesn't exist, clone
if exist "%websiteDest%" (
    echo SearchDex website folder already exists. That won't be updated...
) else (
    echo Cloning SearchDex website files into %websiteDest%...
    git clone --depth 1 %websiteUrl% %websiteDest%
)

REM ======= PNPM STEPS =======
cd /d "%gameDest%"
echo Running game export script
call pnpm --version
call pnpm install
call pnpm species-data:export --json

echo.
echo ======= ALL DONE =======
echo.
pause