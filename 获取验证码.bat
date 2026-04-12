@echo off
chcp 65001 >nul
title 每日验证码生成器 - GUI版
python password_generator_gui.py
if errorlevel 1 (
    echo.
    echo 发生错误，请检查Python环境是否正确安装
    pause
)
