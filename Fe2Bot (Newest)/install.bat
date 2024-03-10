@echo off
color 5
echo Python version:
python --version
echo starting install in 3 seconds
timeout /t 3
echo installing packages.
pip install discord requests srcomapi selenium webdriver-manager
echo done, exiting in 3 seconds.
timeout /t 3