@echo off
chcp 65001 >nul
title 打包企业微信批量发送工具

echo.
echo ================================================
echo    企业微信批量发送工具 - 打包脚本
echo ================================================
echo.
echo 正在清理旧的打包文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo ✓ 清理完成
echo.

echo 开始打包主程序...
pyinstaller --onefile ^
    --windowed ^
    --name="企业微信批量发送工具" ^
    --icon=NONE ^
    --add-data "wecom;wecom" ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=win32clipboard ^
    --hidden-import=keyboard ^
    --hidden-import=hmac ^
    app.py

if errorlevel 1 (
    echo.
    echo ❌ 主程序打包失败！
    pause
    exit /b 1
)

echo ✓ 主程序打包完成
echo.

echo 开始打包验证码生成器（GUI版）...
pyinstaller --onefile ^
    --windowed ^
    --name="获取验证码" ^
    --icon=NONE ^
    --add-data "wecom;wecom" ^
    --hidden-import=hmac ^
    password_generator_gui.py

if errorlevel 1 (
    echo.
    echo ❌ 验证码生成器打包失败！
    pause
    exit /b 1
)

echo ✓ 验证码生成器打包完成
echo.

echo 开始打包验证码生成器（命令行版）...
pyinstaller --onefile ^
    --console ^
    --name="生成验证码-命令行" ^
    --icon=NONE ^
    --add-data "wecom;wecom" ^
    --hidden-import=hmac ^
    password_generator.py

if errorlevel 1 (
    echo.
    echo ❌ 命令行验证码生成器打包失败！
    pause
    exit /b 1
)

echo ✓ 命令行验证码生成器打包完成
echo.

echo ================================================
echo    打包完成！
echo ================================================
echo.
echo 生成的文件位置：
echo   📁 dist\企业微信批量发送工具.exe
echo   📁 dist\获取验证码.exe
echo   📁 dist\生成验证码-命令行.exe
echo.
echo 提示：可以将这些exe文件复制到任意位置使用
echo.
pause
