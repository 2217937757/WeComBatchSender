@echo off
chcp 65001 >nul
echo ================================================
echo    企业微信批量发送工具 - 每日验证码生成器
echo ================================================
echo.
python password_generator.py
echo.
pause
