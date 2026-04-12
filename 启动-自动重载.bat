@echo off
chcp 65001 >nul
title 企业微信批量发送工具 - 自动重载模式
echo.
echo ================================================
echo    企业微信批量发送工具 - 自动重载管理器
echo ================================================
echo.
echo 🔄 程序将在运行12小时后自动重启
echo ⏰ 这样可以确保软件始终保持最佳状态
echo.
echo 按 Ctrl+C 可以随时停止自动重载
echo.
pause
python auto_reload.py
if errorlevel 1 (
    echo.
    echo ❌ 发生错误，请检查Python环境是否正确安装
    pause
)
