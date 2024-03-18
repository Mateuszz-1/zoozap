@echo off
setlocal

set "DIR=%~dp0"

for /L %%i in (1,1,200) do (
    echo Iteration %%i

    start cmd /c "cd "%DIR%" && call env\Scripts\activate && python game/server.py && exit"
    timeout /t 1 /nobreak >nul

    start cmd /c "cd "%DIR%" && call env\Scripts\activate && python ai/random_agent.py && exit"
    start cmd /c "cd "%DIR%" && call env\Scripts\activate && python ai/random_agent.py && exit"

    timeout /t 1 /nobreak >nul
)

endlocal
