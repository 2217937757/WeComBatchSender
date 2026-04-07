@echo off
chcp 65001 >nul
echo ========================================
echo Git 仓库初始化脚本
echo ========================================
echo.

REM 检查是否已初始化
if exist ".git" (
    echo ⚠️  Git 仓库已存在！
    echo.
    choice /C YN /M "是否重新初始化（将删除现有Git历史）"
    if errorlevel 2 goto :end
    if errorlevel 1 (
        echo 正在删除现有 Git 仓库...
        rmdir /s /q .git
        echo ✓ 删除完成
    )
)

echo.
echo [1/4] 初始化 Git 仓库...
git init
echo ✓ Git 仓库已创建
echo.

echo [2/4] 添加所有文件...
git add .
echo ✓ 文件已添加
echo.

echo [3/4] 创建初始提交...
git commit -m "初始提交：企业微信批量发送工具 v1.3"
echo ✓ 初始提交完成
echo.

echo [4/4] 查看状态...
git status
echo.

echo ========================================
echo ✅ Git 仓库初始化完成！
echo ========================================
echo.
echo 💡 下一步：
echo    1. 查看提交历史: git log
echo    2. 添加远程仓库: git remote add origin [URL]
echo    3. 推送到远程: git push -u origin main
echo.
echo 📝 详细说明请查看: GIT_GUIDE.md
echo.
pause

:end
