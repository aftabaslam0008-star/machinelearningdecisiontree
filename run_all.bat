@echo off
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Running Task 1...
python task1_titanic.py
echo.
echo Running Task 2...
python task2_car_safety.py
pause
