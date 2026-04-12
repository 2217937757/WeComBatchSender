"""
企业微信批量发送工具 - GUI 界面
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import keyboard
import queue
import os
import time
import pyautogui

from wecom.utils.contact_extractor import extract_contacts_from_text
from wecom.core.sender import send_to_contact
from wecom.utils.daily_password import verify_password

class WeComApp:
    def __init__(self, root):
        self.root = root
        self.root.title("企业微信批量发送工具 - 集成版")
        
        # 先设置窗口大小并居中
        window_width = 900
        window_height = 850
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # 先显示密码验证对话框
        if not self.show_password_dialog(root):
            root.destroy()
            return

        # 状态变量
        self.is_paused = False
        self.is_running = False
        self.selected_images = []
        self.log_queue = queue.Queue()

        # 启动日志处理器
        self.process_log_queue()

        # 注册热键
        keyboard.add_hotkey('f4', self.toggle_pause)
        keyboard.add_hotkey('esc', self.stop_send)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()

    def log(self, text):
        print(text)
        self.log_queue.put(text + "\n")

    def process_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_box.insert(tk.END, msg)
                self.log_box.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.process_log_queue)

    def show_password_dialog(self, root):
        """
        显示密码验证对话框
        
        Returns:
            bool: 验证是否成功
        """
        dialog = tk.Toplevel(root)
        dialog.title("🔐 身份验证")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        # 居中显示
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # 设置模态窗口
        dialog.transient(root)
        dialog.grab_set()
        
        # 标题
        title_label = ttk.Label(
            dialog, 
            text="🔐 身份验证", 
            font=("微软雅黑", 14, "bold")
        )
        title_label.pack(pady=20)
        
        # 密码输入框
        input_frame = ttk.Frame(dialog)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="验证码:", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(
            input_frame, 
            textvariable=password_var,
            show="*",
            font=("微软雅黑", 11),
            width=15
        )
        password_entry.pack(side=tk.LEFT, padx=5)
        password_entry.focus_set()
        
        # 错误提示标签
        error_label = ttk.Label(
            dialog,
            text="",
            font=("微软雅黑", 9),
            foreground="red"
        )
        error_label.pack(pady=5)
        
        # 按钮框架
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)
        
        verification_success = [False]  # 使用列表以便在闭包中修改
        
        def verify_and_close():
            input_pwd = password_var.get().strip()
            if not input_pwd:
                error_label.config(text="请输入验证码")
                return
            
            if len(input_pwd) != 6:
                error_label.config(text="验证码必须是6位数字")
                return
            
            if verify_password(input_pwd):
                verification_success[0] = True
                dialog.destroy()
            else:
                error_label.config(text="验证码错误，请重试")
                password_var.set("")
                password_entry.focus_set()
        
        def on_enter(event):
            verify_and_close()
        
        password_entry.bind('<Return>', on_enter)
        
        ttk.Button(
            btn_frame,
            text="✓ 验证",
            command=verify_and_close,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="✗ 取消",
            command=lambda: dialog.destroy(),
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # 等待对话框关闭
        root.wait_window(dialog)
        
        return verification_success[0]

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # 标签1：联系人提取
        self.tab_extract = ttk.Frame(notebook)
        notebook.add(self.tab_extract, text='📋 联系人提取')
        self.create_extract_tab()

        # 标签2：批量发送
        self.tab_send = ttk.Frame(notebook)
        notebook.add(self.tab_send, text='📤 批量发送')
        self.create_send_tab()

    def create_extract_tab(self):
        ttk.Label(self.tab_extract, text="从 QQ/微信长截图中提取联系人", 
                 font=("微软雅黑", 12, "bold")).pack(pady=10)
        
        ttk.Label(self.tab_extract, text="步骤：1.长截图 2.识别文字 3.粘贴到下方 4.点击提取", 
                 foreground="gray").pack(pady=5)

        ttk.Label(self.tab_extract, text="原始文本（粘贴在这里）").pack(anchor=tk.W, padx=20, pady=(10,5))
        self.extract_input = scrolledtext.ScrolledText(self.tab_extract, width=110, height=12)
        self.extract_input.pack(padx=20, pady=5)

        btn_frame = ttk.Frame(self.tab_extract)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="🔧 提取联系人", command=self.extract_contacts, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📤 用到发送工具", command=self.use_extracted_contacts, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ 清空", command=self.clear_extract, width=15).pack(side=tk.LEFT, padx=5)

        self.extract_stats = ttk.Label(self.tab_extract, text="", font=("微软雅黑", 10), foreground="blue")
        self.extract_stats.pack(pady=5)

        ttk.Label(self.tab_extract, text="提取结果（每行一个）").pack(anchor=tk.W, padx=20, pady=(10,5))
        self.extract_output = scrolledtext.ScrolledText(self.tab_extract, width=110, height=15, wrap=tk.NONE)
        self.extract_output.pack(padx=20, pady=5)

    def create_send_tab(self):
        ttk.Label(self.tab_send, text="企业微信批量发送工具", 
                 font=("微软雅黑", 12, "bold")).pack(pady=10)

        ttk.Label(self.tab_send, text="💡 提示：程序会自动检测输入内容和已选图片", foreground="gray").pack(anchor=tk.W, padx=20, pady=(5,0))
        ttk.Label(self.tab_send, text="   - 只输入文字 → 发送纯文字", foreground="gray").pack(anchor=tk.W, padx=20)
        ttk.Label(self.tab_send, text="   - 只选择图片 → 发送纯图片", foreground="gray").pack(anchor=tk.W, padx=20)
        ttk.Label(self.tab_send, text="   - 文字+图片 → 发送图文混合消息", foreground="gray").pack(anchor=tk.W, padx=20)

        ttk.Label(self.tab_send, text="发送内容").pack(anchor=tk.W, padx=20, pady=(10,0))
        self.msg_text = scrolledtext.ScrolledText(self.tab_send, width=110, height=5)
        self.msg_text.pack(padx=20, pady=5)
        self.msg_text.insert("1.0", "你好，这是测试消息")

        img_select_frame = ttk.Frame(self.tab_send)
        img_select_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Button(img_select_frame, text="📁 选择图片", command=self.select_images, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(img_select_frame, text="❌ 移除选中", command=self.remove_selected_image, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(img_select_frame, text="🗑️ 清空全部", command=self.clear_all_images, width=12).pack(side=tk.LEFT, padx=2)

        ttk.Label(self.tab_send, text="已选图片列表").pack(anchor=tk.W, padx=20, pady=(5,0))
        self.image_list = tk.Listbox(self.tab_send, width=108, height=3)
        self.image_list.pack(padx=20, pady=5)

        ttk.Label(self.tab_send, text="联系人名称（每行一个）").pack(anchor=tk.W, padx=20)
        self.names_text = scrolledtext.ScrolledText(self.tab_send, width=110, height=10, wrap=tk.NONE)
        self.names_text.pack(padx=20, pady=5)
        self.names_text.insert("1.0", "小刀\n开发测试用")

        delay_frame = ttk.Frame(self.tab_send)
        delay_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(delay_frame, text="延时配置(秒):").pack(side=tk.LEFT)
        ttk.Label(delay_frame, text="粘贴后:").pack(side=tk.LEFT, padx=(10,2))
        self.paste_delay_entry = ttk.Entry(delay_frame, width=6)
        self.paste_delay_entry.pack(side=tk.LEFT)
        self.paste_delay_entry.insert(0, "0.2")
        ttk.Label(delay_frame, text="发送后:").pack(side=tk.LEFT, padx=(10,2))
        self.send_delay_entry = ttk.Entry(delay_frame, width=6)
        self.send_delay_entry.pack(side=tk.LEFT)
        self.send_delay_entry.insert(0, "0.4")
        ttk.Label(delay_frame, text="切换:").pack(side=tk.LEFT, padx=(10,2))
        self.nav_delay_entry = ttk.Entry(delay_frame, width=6)
        self.nav_delay_entry.pack(side=tk.LEFT)
        self.nav_delay_entry.insert(0, "0.3")

        send_btn_frame = ttk.Frame(self.tab_send)
        send_btn_frame.pack(pady=8)
        self.btn_start = ttk.Button(send_btn_frame, text="▶ 开始运行", command=self.start_thread)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        ttk.Button(send_btn_frame, text="⏹ 停止", command=self.stop_send).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.tab_send, text="运行日志（F4 暂停/继续 | ESC 停止）").pack(anchor=tk.W, padx=20)
        self.log_box = scrolledtext.ScrolledText(self.tab_send, width=110, height=14)
        self.log_box.pack(padx=20, pady=5)

    # --- 联系人提取逻辑 ---
    def extract_contacts(self):
        raw_text = self.extract_input.get("1.0", tk.END)
        contacts = extract_contacts_from_text(raw_text)
        
        result_text = '\n'.join(contacts)
        self.extract_output.delete("1.0", tk.END)
        self.extract_output.insert("1.0", result_text)
        self.extract_stats.config(text=f"提取到 {len(contacts)} 个联系人/群（已去重）")
        
        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        messagebox.showinfo("完成", f"✓ 提取到 {len(contacts)} 个联系人\n已自动复制到剪贴板")

    def clear_extract(self):
        self.extract_input.delete("1.0", tk.END)
        self.extract_output.delete("1.0", tk.END)
        self.extract_stats.config(text="")

    def use_extracted_contacts(self):
        contacts = self.extract_output.get("1.0", tk.END).strip()
        if contacts:
            self.names_text.delete("1.0", tk.END)
            self.names_text.insert("1.0", contacts)
            # 切换到发送标签
            for i, tab in enumerate(self.root.children.values()):
                if isinstance(tab, ttk.Notebook):
                    tab.select(1)
            messagebox.showinfo("提示", "已将联系人复制到发送工具")
        else:
            messagebox.showwarning("提示", "没有可使用的联系人")

    # --- 图片管理逻辑 ---
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"), ("所有文件", "*.*")]
        )
        if files:
            self.selected_images.extend(files)
            self.update_image_list()
            self.log(f"✓ 已添加 {len(files)} 张图片")

    def remove_selected_image(self):
        selection = self.image_list.curselection()
        if selection:
            index = selection[0]
            removed = self.selected_images.pop(index)
            self.update_image_list()
            self.log(f"✓ 已移除: {os.path.basename(removed)}")

    def clear_all_images(self):
        self.selected_images.clear()
        self.update_image_list()
        self.log("✓ 已清空所有图片")

    def update_image_list(self):
        self.image_list.delete(0, tk.END)
        for img_path in self.selected_images:
            filename = os.path.basename(img_path)
            self.image_list.insert(tk.END, f"📷 {filename}")

    # --- 批量发送逻辑 ---
    def start_send(self):
        if self.is_running:
            self.log("【警告】已在运行中")
            return

        msg = self.msg_text.get("1.0", tk.END).strip()
        names_str = self.names_text.get("1.0", tk.END).strip()
        
        if not names_str:
            self.log("【错误】请输入联系人名称")
            return
        
        names = [name.strip() for name in names_str.split('\n') if name.strip()]
        if not names:
            self.log("【错误】联系人列表为空")
            return
        
        send_text = bool(msg.strip()) if msg else False
        send_images = len(self.selected_images) > 0
        
        if not send_text and not send_images:
            self.log("【错误】请输入文字或选择图片")
            return

        try:
            delays = {
                'paste': float(self.paste_delay_entry.get()),
                'send': float(self.send_delay_entry.get()),
                'nav': float(self.nav_delay_entry.get())
            }
        except:
            self.log("【错误】延时配置必须是数字")
            return

        self.is_running = True
        self.is_paused = False
        self.btn_start.config(state=tk.DISABLED, text="运行中")

        self.log("=" * 50)
        self.log(f"发送人数：{len(names)}")
        self.log(f"发送内容：{'文字' if send_text else ''} {'+图片' if send_images else ''}")
        if send_images:
            self.log(f"图片数量：{len(self.selected_images)}")
        self.log("正在激活企业微信...")
        self.log("F4 暂停/继续 | ESC 紧急停止")
        self.log("=" * 50)

        try:
            pyautogui.hotkey('alt', 'shift', 's')
            time.sleep(0.6)
            
            for i in range(3, 0, -1):
                self.log(f"倒计时：{i}")
                time.sleep(1)

            for i, name in enumerate(names):
                if not self.is_running:
                    self.log("\n⚠️ 已手动停止")
                    break

                while self.is_paused:
                    time.sleep(0.2)
                    if not self.is_running:
                        break

                if not self.is_running:
                    break

                self.log(f"\n→ 发送第 {i+1}/{len(names)} 人：{name}")
                
                current_msg = msg if send_text else ""
                current_images = self.selected_images if send_images else []
                
                success = send_to_contact(
                    name, current_msg, current_images, delays, 
                    log_callback=self.log,
                    stop_check=lambda: not self.is_running
                )
                
                if not success:
                    break
                
                time.sleep(delays['nav'])

            if self.is_running:
                self.log("\n🎉 全部发送完成！")
                pyautogui.press('esc')
                time.sleep(0.2)
                pyautogui.press('esc')
                time.sleep(0.3)
                self.log("✓ 已关闭企业微信")
        
        except Exception as e:
            self.log(f"【严重错误】{str(e)}")
        finally:
            self.is_running = False
            self.btn_start.config(state=tk.NORMAL, text="▶ 开始运行")

    def start_thread(self):
        t = threading.Thread(target=self.start_send, daemon=False)
        t.start()

    def stop_send(self):
        if self.is_running:
            self.is_running = False
            self.is_paused = False
            self.log("\n【系统】正在停止...")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.log(f"【系统】{'已暂停' if self.is_paused else '已继续'}")

    def on_closing(self):
        if self.is_running:
            if messagebox.askokcancel("退出", "正在运行中，确定要退出吗？"):
                self.is_running = False
                self.root.destroy()
        else:
            self.root.destroy()
