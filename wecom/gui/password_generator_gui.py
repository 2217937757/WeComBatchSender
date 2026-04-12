"""
每日密码生成器 - GUI版本
提供图形化界面显示和复制今日验证码
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wecom.utils.daily_password import get_today_password, get_totp_remaining_time


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 动态验证码生成器 (TOTP)")
        self.root.geometry("500x520")
        self.root.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 创建界面
        self.create_widgets()
        
        # 显示当前密码
        self.display_password()
        
        # 启动定时器，每秒更新倒计时
        self.update_countdown()
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text="🔐 企业微信批量发送工具",
            font=("微软雅黑", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="每日验证码生成器",
            font=("微软雅黑", 11),
            foreground="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # 密码显示区域
        password_frame = ttk.LabelFrame(main_frame, text="今日验证码", padding=15)
        password_frame.pack(fill=tk.X, pady=10)
        
        # 密码标签
        self.password_var = tk.StringVar()
        password_label = ttk.Label(
            password_frame,
            textvariable=self.password_var,
            font=("Consolas", 36, "bold"),
            foreground="#e74c3c",
            justify=tk.CENTER
        )
        password_label.pack(pady=10)
        
        # 日期显示（改为显示刷新时间）
        remaining = get_totp_remaining_time()
        self.time_var = tk.StringVar()
        self.time_var.set(f"下次刷新: {remaining} 秒")
        time_label = ttk.Label(
            password_frame,
            textvariable=self.time_var,
            font=("微软雅黑", 9),
            foreground="#3498db"
        )
        time_label.pack(pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        # 复制按钮
        copy_btn = ttk.Button(
            btn_frame,
            text="📋 复制验证码",
            command=self.copy_password,
            width=15
        )
        copy_btn.pack(side=tk.LEFT, padx=10, expand=True, ipady=8)
        
        # 刷新按钮
        refresh_btn = ttk.Button(
            btn_frame,
            text="🔄 刷新",
            command=self.refresh_password,
            width=15
        )
        refresh_btn.pack(side=tk.LEFT, padx=10, expand=True, ipady=8)
        
        # 说明文本
        info_text = (
            "💡 使用说明：\n"
            "1. 验证码每30秒自动刷新一次\n"
            "2. 前后30秒内都有效（共90秒）\n"
            "3. 点击「复制验证码」按钮复制\n"
            "4. 打开企业微信批量发送工具\n"
            "5. 在验证对话框中粘贴并输入"
        )
        info_label = ttk.Label(
            main_frame,
            text=info_text,
            font=("微软雅黑", 9),
            foreground="#34495e",
            justify=tk.LEFT,
            wraplength=450
        )
        info_label.pack(pady=10)
        
        # 底部提示
        footer_label = ttk.Label(
            main_frame,
            text="⚠️ 请妥善保管验证码，不要泄露给他人",
            font=("微软雅黑", 8),
            foreground="#e67e22"
        )
        footer_label.pack(pady=5)
    
    def display_password(self):
        """显示当前密码"""
        password = get_today_password()
        self.password_var.set(password)
    
    def update_countdown(self):
        """更新倒计时显示"""
        remaining = get_totp_remaining_time()
        self.time_var.set(f"下次刷新: {remaining} 秒")
        
        # 如果剩余时间小于5秒，改变颜色提醒
        if remaining <= 5:
            self.time_var.set(f"⚠️ 即将刷新: {remaining} 秒")
        
        # 每秒更新一次
        self.root.after(1000, self.update_countdown)
    
    def copy_password(self):
        """复制密码到剪贴板"""
        password = self.password_var.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()
        
        messagebox.showinfo(
            "复制成功",
            f"✓ 验证码 {password} 已复制到剪贴板\n\n请直接粘贴到验证对话框中",
            parent=self.root
        )
    
    def refresh_password(self):
        """刷新密码显示"""
        self.display_password()
        messagebox.showinfo(
            "刷新成功",
            "✓ 验证码已刷新",
            parent=self.root
        )


def main():
    """主函数"""
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
