# 📦 打包指南

## 🚀 30秒快速打包

```bash
# 1. 安装 PyInstaller（首次需要）
pip install pyinstaller

# 2. 双击运行 build.bat
# 或者在命令行运行：
build.bat

# 3. 等待1-3分钟
# 4. 在 dist 文件夹找到 exe 文件
```

**就这么简单！** 🎉

---

## 详细指南

## 方法一：使用自动打包脚本（推荐）⭐

### Windows 用户

1. **双击运行** `build.bat`
2. 等待打包完成（约1-3分钟）
3. 在 `dist` 文件夹中找到 `企业微信批量发送工具.exe`

### 注意事项

- ✅ 首次打包需要安装 PyInstaller：`pip install pyinstaller`
- ✅ 打包过程中会显示进度
- ✅ 完成后自动生成可执行文件

---

## 方法二：手动打包

### 步骤1：安装 PyInstaller

```bash
pip install pyinstaller
```

### 步骤2：执行打包命令

```bash
pyinstaller --onefile --windowed --name="企业微信批量发送工具" app.py
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--onefile` | 打包成单个exe文件 |
| `--windowed` | 不显示控制台窗口 |
| `--name` | 指定生成的exe文件名 |
| `--icon` | 指定图标文件（可选） |

---

## 📂 打包后的文件结构

```
dist/
└── 企业微信批量发送工具.exe    ← 分享给别人的文件
```

**建议分享方式：**
```
企业微信批量发送工具/
├── 企业微信批量发送工具.exe    ← 主程序
├── README.md                    ← 使用说明
├── QUICKSTART.md                ← 快速开始
└── QQ_SCREENSHOT_GUIDE.md       ← 长截图教程
```

---

## ⚠️ 常见问题

### Q1: 打包后文件很大（约200-300MB）？

**原因**：PyInstaller 会打包 Python 解释器和所有依赖库

**解决**：这是正常的，可以使用以下方法减小体积：
```bash
# 使用 UPX 压缩（需要先安装 UPX）
pyinstaller --onefile --windowed --upx-dir=upx路径 app.py
```

### Q2: 杀毒软件报毒？

**原因**：PyInstaller 打包的程序可能被误判

**解决**：
1. 添加到杀毒软件白名单
2. 使用代码签名证书（专业方案）
3. 告知用户这是安全工具

### Q3: 运行时提示缺少模块？

**解决**：确保所有依赖都已正确导入
```bash
# 检查是否有隐藏导入
pyinstaller --onefile --windowed \
    --hidden-import=tkinter \
    --hidden-import=pyperclip \
    --hidden-import=pyautogui \
    --hidden-import=keyboard \
    app.py
```

### Q4: 首次运行很慢？

**原因**：解压临时文件

**解决**：正常现象，后续运行会快很多

---

## 🎯 分发建议

### 方案A：直接分享 exe（简单）

**优点**：
- ✅ 最简单
- ✅ 用户无需安装任何东西

**缺点**：
- ❌ 文件较大（200-300MB）
- ❌ 可能被杀毒软件拦截

**适用**：小范围分享、内部使用

---

### 方案B：制作安装包（专业）

**工具推荐**：
- **Inno Setup**（免费，Windows）
- **NSIS**（免费，Windows）
- **InstallShield**（付费，专业）

**优点**：
- ✅ 可以添加卸载功能
- ✅ 可以创建桌面快捷方式
- ✅ 更专业的用户体验

**适用**：正式产品、大范围分发

---

### 方案C：提供源码 + 安装说明（开放）

**包含内容**：
```
项目文件夹/
├── app.py
├── requirements.txt
├── README.md
└── 安装说明.txt
```

**安装说明.txt**：
```
1. 安装 Python 3.8+
2. 运行：pip install -r requirements.txt
3. 运行：python app.py
```

**优点**：
- ✅ 文件小
- ✅ 透明可信
- ✅ 易于更新

**缺点**：
- ❌ 用户需要安装 Python
- ❌ 操作步骤较多

**适用**：技术人员、开源项目

---

## 💡 最佳实践

### 对于内部使用（推荐方案A）

1. 运行 `build.bat` 打包
2. 将 `dist` 文件夹压缩成 zip
3. 通过邮件/网盘分享给同事
4. 附带简单的使用说明

### 对于外部用户（推荐方案B）

1. 使用 Inno Setup 制作安装包
2. 添加版本信息和更新日志
3. 提供在线下载链接
4. 建立用户反馈渠道

---

## 🔧 高级配置

### 添加图标

准备一个 `.ico` 文件（256x256像素）：

```bash
pyinstaller --onefile --windowed --icon=app.ico app.py
```

### 添加版本信息

创建 `version_info.txt`：

```python
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 3, 0, 0),
    prodvers=(1, 3, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'企业微信批量发送工具'),
        StringStruct(u'FileVersion', u'1.3.0.0'),
        StringStruct(u'InternalName', u'app'),
        StringStruct(u'LegalCopyright', u'Copyright © 2026'),
        StringStruct(u'OriginalFilename', u'app.exe'),
        StringStruct(u'ProductName', u'企业微信批量发送工具'),
        StringStruct(u'ProductVersion', u'1.3.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)
```

然后打包时添加：
```bash
pyinstaller --onefile --windowed --version-file=version_info.txt app.py
```

---

## 📊 打包效果对比

| 方式 | 文件大小 | 易用性 | 专业性 | 推荐场景 |
|------|---------|--------|--------|----------|
| **单文件exe** | 200-300MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 内部分享 |
| **安装包** | 200-300MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 正式发布 |
| **源码+说明** | <1MB | ⭐⭐ | ⭐⭐⭐ | 技术交流 |

---

## ✅ 打包检查清单

打包前确认：

- [ ] 代码已测试无误
- [ ] 所有依赖已安装
- [ ] README 等文档已更新
- [ ] 版本号已更新
- [ ] CHANGELOG 已记录
- [ ] 已清理临时文件

打包后确认：

- [ ] exe 能正常运行
- [ ] 所有功能正常
- [ ] 文件大小合理
- [ ] 无杀毒软件误报（或已处理）
- [ ] 文档齐全

---

**祝你打包顺利！** 🎉
