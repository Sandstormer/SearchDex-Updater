@echo off
setlocal enabledelayedexpansion

REM ======= CONFIG =======
set "branchName=wiki-scraper"
set "repoUrl=https://github.com/fabske0/pokerogue.git"
set "repoDest=game_files"

set "websiteUrl=https://github.com/Sandstormer/PokeRogue-Dex.git"
set "websiteDest=website"

REM ======= CLONE / UPDATE GAME FILES =======
call :clone_or_update "%repoUrl%" "%repoDest%" "%branchName%" 0

REM ======= CLONE WEBSITE (ONLY ONCE) =======
call :clone_or_update "%websiteUrl%" "%websiteDest%" "" 1

REM ======= PNPM STEPS =======
cd /d "%repoDest%" || exit /b 1
pnpm --version || exit /b 1
pnpm install || exit /b 1
pnpm wiki-scrape --json || exit /b 1

echo.
echo ======= ALL DONE =======
echo.
pause
exit /b 0


REM =========================================================
REM FUNCTION: clone_or_update repoUrl repoDest branch onlyClone
REM onlyClone: 1 = never update if exists, 0 = allow update
REM =========================================================
:clone_or_update
set "url=%~1"
set "dest=%~2"
set "branch=%~3"
set "onlyClone=%~4"

echo.
echo ================================
echo Processing %dest%
echo ================================

REM If folder doesn't exist -> clone
if not exist "%dest%" (
    echo Cloning repository into %dest%...

    if not "%branch%"=="" (
        git clone --depth 1 -b %branch% --shallow-submodules --recursive %url% %dest%
    ) else (
        git clone --depth 1 %url% %dest%
    )

    exit /b 0
)

REM If onlyClone mode is enabled -> do NOT update
if "%onlyClone%"=="1" (
    echo %dest% already exists. Skipping update...
    exit /b 0
)

REM If folder exists but is NOT a git repo
if not exist "%dest%\.git" (
    echo Folder exists at %dest% but is not a git repository.
    echo Delete it manually to continue.
    pause
    exit /b 1
)

echo Resetting repository at %dest%...

git -C "%dest%" fetch --depth 1 origin || exit /b 1

if not "%branch%"=="" (
    git -C "%dest%" fetch --depth 1 origin %branch% || exit /b 1
    git -C "%dest%" checkout -B %branch% FETCH_HEAD || exit /b 1
) else (
    git -C "%dest%" reset --hard origin/HEAD || exit /b 1
)

git -C "%dest%" clean -fdx || exit /b 1

git -C "%dest%" submodule update --init --recursive --force --depth 1 || exit /b 1

exit /b 0