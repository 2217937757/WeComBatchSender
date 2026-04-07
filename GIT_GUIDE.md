# Git 使用指南

## 📋 已配置忽略的文件

以下文件/文件夹不会被提交到 Git：

### 打包相关文件
- ✅ `dist/` - 打包生成的exe文件
- ✅ `build/` - PyInstaller 临时文件
- ✅ `*.spec` - PyInstaller 配置文件

### Python 临时文件
- ✅ `__pycache__/` - Python 缓存
- ✅ `*.pyc`, `*.pyo` - 编译文件
- ✅ `*.egg-info/` - 包信息

### 虚拟环境
- ✅ `venv/`, `env/` - 虚拟环境文件夹

### IDE 配置
- ✅ `.vscode/` - VSCode 配置
- ✅ `.idea/` - PyCharm 配置
- ✅ `.lingma/` - Lingma IDE 配置

### 临时文件
- ✅ `temp_contact.png` - OCR 临时截图
- ✅ `contacts_extracted.txt` - 提取的原始联系人
- ✅ `contacts_clean.txt` - 清理后的联系人

---

## 🚀 Git 基本操作

### 初始化仓库（首次）

```bash
git init
git add .
git commit -m "初始提交：企业微信批量发送工具 v1.3"
```

### 日常提交

```bash
# 查看修改
git status

# 添加所有修改
git add .

# 提交
git commit -m "更新说明：添加了打包功能"

# 推送到远程（如果配置了）
git push
```

### 查看历史

```bash
# 查看提交历史
git log

# 简洁模式
git log --oneline
```

---

## 💡 最佳实践

### 提交前检查

```bash
# 1. 查看哪些文件会被提交
git status

# 2. 确认没有包含：
#    - dist/ 文件夹
#    - build/ 文件夹
#    - *.exe 文件
#    - __pycache__/ 文件夹
```

### 提交消息规范

```bash
# 格式：类型: 简短描述

git commit -m "功能: 添加联系人提取功能"
git commit -m "修复: 解决时间戳识别问题"
git commit -m "文档: 更新README和打包指南"
git commit -m "优化: 改进GUI界面布局"
```

### 版本标签

```bash
# 打标签
git tag -a v1.3 -m "发布 v1.3 集成版"

# 查看标签
git tag

# 推送标签
git push origin v1.3
```

---

## ⚠️ 注意事项

### 不要提交的文件

❌ **绝对不要提交：**
- `dist/` 文件夹（包含exe，体积大）
- `build/` 文件夹（临时文件）
- `venv/` 文件夹（虚拟环境）
- `__pycache__/` 文件夹（Python缓存）
- `.exe` 文件（应该通过打包脚本生成）

✅ **应该提交：**
- 源代码（`.py` 文件）
- 文档（`.md` 文件）
- 配置文件（`requirements.txt`, `.gitignore`）
- 打包脚本（`build.bat`）

---

## 🔧 如果误提交了文件

### 从 Git 中移除（但保留本地文件）

```bash
# 移除 dist 文件夹
git rm -r --cached dist/

# 移除 build 文件夹
git rm -r --cached build/

# 移除所有 exe 文件
git rm --cached *.exe

# 提交更改
git commit -m "清理：移除不应提交的文件"
```

### 完全删除（包括本地文件）

```bash
# 警告：这会删除本地文件！
git rm -r dist/
git commit -m "删除dist文件夹"
```

---

## 📦 推荐的项目结构

```
WeComBatchSender/
├── .git/                  # Git 仓库（隐藏）
├── .gitignore             # Git 忽略规则 ✅
├── app.py                 # 主程序 ✅
├── main.py                # 独立版发送工具 ✅
├── contact_cleaner.py     # 独立版提取工具 ✅
├── build.bat              # 打包脚本 ✅
├── requirements.txt       # 依赖列表 ✅
├── README.md              # 主文档 ✅
├── QUICKSTART.md          # 快速指南 ✅
├── QQ_SCREENSHOT_GUIDE.md # 长截图教程 ✅
├── BUILD_GUIDE.md         # 打包指南 ✅
├── CHANGELOG.md           # 更新日志 ✅
├── 分享说明.txt            # 分发说明 ✅
└── dist/                  # ❌ 被忽略（不提交）
    └── 企业微信批量发送工具.exe
```

---

## 🎯 协作建议

### 分享给团队成员

**方式A：Git 仓库**
```bash
# 推送到 GitHub/Gitee
git remote add origin https://github.com/yourname/WeComBatchSender.git
git push -u origin main

# 团队成员克隆
git clone https://github.com/yourname/WeComBatchSender.git
```

**方式B：直接分享代码**
- 压缩除了 `dist/` 和 `build/` 的所有文件
- 对方解压后运行 `pip install -r requirements.txt`
- 然后可以自行打包

---

## 📊 Git 状态检查清单

提交前确认：

- [ ] 运行 `git status` 查看变更
- [ ] 确认 `dist/` 不在待提交列表中
- [ ] 确认 `build/` 不在待提交列表中
- [ ] 确认没有 `.exe` 文件
- [ ] 代码已测试通过
- [ ] 文档已更新
- [ ] 版本号已更新
- [ ] CHANGELOG 已记录

---

**祝 Git 使用顺利！** 🎉
