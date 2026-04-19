@echo off

set results=.\results
set rep_history=.\final-report\history
set report=.\final-report


if exist %results% rmdir /s /q %results% 2>nul
if "%1"=="ui" (
    echo ========================================
    echo Running UI tests only...
    echo ========================================
    pytest -m "ui" --alluredir=%results% -v
    goto generate
)

if "%1"=="api" (
    echo ========================================
    echo Running API tests only...
    echo ========================================
    pytest  -m "api" --alluredir=%results% -v
    goto generate
)

if "%1"=="all" (
    echo ========================================
    echo Running ALL tests...
    echo ========================================
    pytest --alluredir=%results% -v
    goto generate
)

echo ========================================
echo Usage: run.bat [ui^|api^|all]
echo ========================================
echo   run.bat ui   - запуск только UI тестов
echo   run.bat api  - запуск только API тестов
echo   run.bat all  - запуск всех тестов
echo ========================================
exit /b 1

:generate
if exist %rep_history% (
    xcopy %rep_history% %results%\history /E /I /Y >nul
)

if exist %report% rmdir /s /q %report% 2>nul
allure generate %results% -o %report%
allure open final-report
