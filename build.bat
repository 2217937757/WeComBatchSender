@echo off
chcp 65001 >nul
echo ========================================
echo 企业微信批量发送工具 - 打包脚本
echo ========================================
echo.

echo [1/3] 清理旧文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"
echo ✓ 清理完成
echo.

echo [2/3] 开始打包主程序...
pyinstaller --onefile ^
    --windowed ^
    --name="企业微信批量发送工具" ^
    --icon=NONE ^
    --add-data "wecom;wecom" ^
    --hidden-import=tkinter ^
    --hidden-import=pyperclip ^
    --hidden-import=pyautogui ^
    --hidden-import=keyboard ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=win32clipboard ^
    --hidden-import=win32con ^
    --hidden-import=hmac ^
    app.py

echo.
echo [3/3] 打包完成！
echo.
echo 📦 可执行文件位置: dist\企业微信批量发送工具.exe
echo.
echo 💡 提示：
echo    - 如需打包验证码工具，请运行 build_all.bat
echo    - 该脚本会同时打包主程序和验证码生成器
echo.
echo ⚠️  注意事项：
echo    1. 首次运行可能需要几秒加载
echo    2. 某些杀毒软件可能误报，请添加信任
echo    3. 建议先测试再正式使用
echo.
pause
