# 🚀 快速开始指南

## 💡 推荐：使用集成版

**最简单的方式，一个工具搞定所有！**

```bash
python app.py
```

**功能：**
- 📋 联系人提取
- 📤 批量发送
- 🔄 无缝衔接

---

## 你想做什么？

### 场景1：我已经有联系人名单，想批量发送消息

**只需3步：**

```bash
# 1. 安装依赖
pip install pyperclip pyautogui keyboard

# 2. 运行发送工具
python main.py

# 3. 填写信息并开始发送
```

📖 详细说明：[README.md](README.md)

---

### 场景2：我有1000+联系人，需要提取名单

**推荐方案：QQ/微信长截图**

```bash
# 1. 使用 QQ/微信长截图截取联系人列表
# 2. 右键识别文字并复制
# 3. 运行整理工具
python contact_cleaner.py
# 4. 粘贴 → 整理提取（自动识别时间戳、清理符号）
# 5. 复制到 main.py 中使用
```

⏱️ **耗时**：1000人约10-15分钟  
🎯 **准确率**：95%+  
📖 详细教程：[QQ_SCREENSHOT_GUIDE.md](QQ_SCREENSHOT_GUIDE.md)

---

### 场景3：我想了解完整功能

📖 查看主文档：[README.md](README.md)

---

## 📂 文件说明

| 文件 | 用途 | 何时使用 |
|------|------|----------|
| **main.py** | 批量发送消息 | 已有联系人名单时 |
| **contact_cleaner.py** | 整理联系人名单 | 从截图中提取联系人后 |
| **README.md** | 完整使用说明 | 首次使用必读 |
| **QQ_SCREENSHOT_GUIDE.md** | 长截图提取教程 | 需要提取大量联系人时 |
| **requirements.txt** | Python依赖 | 安装依赖时 |

---

## ⚡ 最常用命令

```bash
# 安装依赖
pip install pyperclip pyautogui keyboard

# 批量发送
python main.py

# 整理联系人
python contact_cleaner.py
```

---

## ❓ 常见问题速查

**Q: 如何获取1000+联系人？**  
A: 使用 QQ 长截图 + contact_cleaner.py，详见 [QQ_SCREENSHOT_GUIDE.md](QQ_SCREENSHOT_GUIDE.md)

**Q: 发送时找不到联系人？**  
A: 确保姓名与企业微信中完全一致

**Q: 想暂停/停止？**  
A: F4 暂停/继续，ESC 紧急停止

**Q: 可以发送图片吗？**  
A: ✅ 支持！可以选择多张图片，支持纯图片发送或图文混合发送。发送时会先粘贴图片，再粘贴文字，最后统一发送为一条消息。

**Q: 如何打包成exe分享给别人？**  
A: 运行 `build.bat` 或查看 [BUILD_GUIDE.md](BUILD_GUIDE.md)

---

## 💡 提示

- ✅ 首次使用建议先用2-3人测试
- ✅ 保持企业微信窗口激活
- ✅ 妥善保管联系人名单
- ✅ 合理使用，勿用于骚扰

---

**祝你使用顺利！** 🎉
