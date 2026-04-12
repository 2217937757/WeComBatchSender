"""
每日验证码生成器 - GUI版主入口
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wecom.gui.password_generator_gui import PasswordGeneratorApp
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
