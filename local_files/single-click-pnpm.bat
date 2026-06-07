@echo off
setlocal

set NODE_VERSION=v22.15.0
set GIT_VERSION=2.54.0
set BRANCH_NAME=wiki-scraper
set REPO_URL=https://github.com/fabske0/pokerogue.git

REM ~~~~~~~ Paths ~~~~~~~
set TOOLS_DIR=.tools
set NODE_DIR=%TOOLS_DIR%\node
mkdir %TOOLS_DIR% 2>nul

if exist "game_files" (
  echo Updating game files...
  git -C "game_files" fetch --depth 1 origin
  pause
  if NOT "%BRANCH_NAME%" == "" (
    echo 7
    git -C "game_files" fetch --depth 1 origin %BRANCH_NAME%
    subprocess.run(["git", "-C", repo_dest, "checkout", "-B", branch_name, "FETCH_HEAD"],)
  ) else (
    subprocess.run(["git", "-C", repo_dest, "reset", "--hard", "origin/HEAD"],)
  )
  pause
    REM Clean any untracked files/directories
    subprocess.run(["git", "-C", repo_dest, "clean", "-fd"],)
    REM Initialize and update submodules recursively, force any local changes to be discarded
    subprocess.run(["git", "-C", repo_dest, "submodule", "update", "--init", "--recursive", "--force", "--depth", "1"],)

) else (
  echo Cloning game files...
  pause
  git clone --depth 1 -b branch_name --shallow-submodules --recursive repo_url repo_dest
)
pause

REM ~~~~~~~ Portable Node.js ~~~~~~~
if not exist "%NODE_DIR%\node.exe" (
  echo Downloading Node.js...
  powershell -Command "Invoke-WebRequest https://nodejs.org/dist/%NODE_VERSION%/node-%NODE_VERSION%-win-x64.zip -OutFile node.zip"
  powershell -Command "Expand-Archive node.zip %TOOLS_DIR% -Force"
  ren "%TOOLS_DIR%\node-%NODE_VERSION%-win-x64" node
  del node.zip
) else (
  echo Node.js is already installed ...
)

REM ~~~~~~~ Portable Git ~~~~~~~
if not exist "%TOOLS_DIR%\git\bin\git.exe" (
    echo Downloading PortableGit...
    powershell -Command "Invoke-WebRequest https://github.com/git-for-windows/git/releases/download/v%GIT_VERSION%.windows.1/PortableGit-%GIT_VERSION%-64-bit.7z.exe -OutFile git.exe"
    echo Extracting Git...
    git.exe -o"%TOOLS_DIR%\git" -y
    del git.exe
) else (
  echo Git is already installed ...
)

REM ~~~~~~~ Add portable installs to PATH ~~~~~~~
set PATH=%CD%\%NODE_DIR%;%CD%\%TOOLS_DIR%\git\bin;%CD%\%TOOLS_DIR%\git\cmd;%PATH%

REM ~~~~~~~ Enable pnpm via Corepack ~~~~~~~
cd game_files
echo.
echo Enabling pnpm...
call corepack enable
call corepack prepare pnpm@latest --activate

REM ~~~~~~~ Verify portable installs are being used ~~~~~~~
echo.
git --version
where git
call pnpm -v
where pnpm
node -v
where node
echo.

REM ~~~~~~~ Install dependencies ~~~~~~~
set GIT_DIR=
set GIT_WORK_TREE=
call pnpm install

REM ~~~~~~~ If you want csv output instead, then remove "--json" from the command below
call pnpm wiki-scrape --json

echo.
echo ~~~~~~~ ALL DONE ~~~~~~~
echo.
pause