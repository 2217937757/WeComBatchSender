"""
企业微信批量发送工具 - 集成版主入口
"""
import tkinter as tk
from wecom.gui.app_window import WeComApp

if __name__ == "__main__":
    root = tk.Tk()
    app = WeComApp(root)
    root.mainloop()
