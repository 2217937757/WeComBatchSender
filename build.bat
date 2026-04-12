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

echo [2/3] 开始打包 app.py...
pyinstaller --onefile ^
    --windowed ^
    --name="企业微信批量发送工具" ^
    --icon=NONE ^
    --add-data "README.md;." ^
    --add-data "QUICKSTART.md;." ^
    --add-data "QQ_SCREENSHOT_GUIDE.md;." ^
    --hidden-import=tkinter ^
    --hidden-import=pyperclip ^
    --hidden-import=pyautogui ^
    --hidden-import=keyboard ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=win32clipboard ^
    --hidden-import=win32con ^
    app.py

echo.
echo [3/3] 打包完成！
echo.
echo 📦 可执行文件位置: dist\企业微信批量发送工具.exe
echo.
echo 💡 分享建议：
echo    1. 将 dist 文件夹中的 exe 和文档一起压缩
echo    2. 建议包含：exe + README.md + QUICKSTART.md
echo    3. 或者使用根目录的“分享说明.txt”
echo.
echo ⚠️  注意事项：
echo    1. 首次运行可能需要几秒加载
echo    2. 某些杀毒软件可能误报，请添加信任
echo    3. 建议先测试再正式使用
echo.
pause
