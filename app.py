"""
企业微信批量发送工具 - 集成版
包含：联系人提取 + 批量发送
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip
import time
import pyautogui
import threading
import keyboard
import queue
import re

# ==================== 全局变量 ====================
is_paused = False
is_running = False
log_queue = queue.Queue()

# ==================== 日志系统 ====================
def log(text):
    """线程安全的日志函数"""
    log_queue.put(text + "\n")

def process_log_queue():
    """主线程定期处理日志队列"""
    try:
        while True:
            msg = log_queue.get_nowait()
            log_box.insert(tk.END, msg)
            log_box.see(tk.END)
    except queue.Empty:
        pass
    root.after(100, process_log_queue)

# ==================== 联系人提取功能 ====================
def extract_contacts():
    """从粘贴的文本中提取联系人"""
    raw_text = extract_input.get("1.0", tk.END)
    
    if not raw_text.strip():
        messagebox.showwarning("提示", "请先粘贴文本")
        return
    
    lines = raw_text.split('\n')
    contacts = []
    
    # 时间戳匹配模式
    time_patterns = [
        r'^\d{1,2}:\d{2}',
        r'^昨天\d{1,2}:\d{2}',
        r'^星期[一二三四五六日天]',
        r'^\d{2}/\d{2}',
        r'^\d+分钟前',
        r'^\d+小时前',
        r'^昨天',
        r'^前天',
    ]
    
    def is_timestamp(line):
        for pattern in time_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    for i in range(len(lines)):
        line = lines[i].strip()
        
        if is_timestamp(line):
            if i >= 2:
                contact_line = lines[i - 2].strip()
                if contact_line:
                    # 清理多余符号
                    contact_line = contact_line.replace('@微信', '').replace('@...', '').replace('@', '')
                    contact_line = contact_line.strip()
                    if contact_line:
                        contacts.append(contact_line)
    
    # 显示结果
    result_text = '\n'.join(contacts)
    extract_output.delete("1.0", tk.END)
    extract_output.insert("1.0", result_text)
    
    # 更新统计
    extract_stats.config(text=f"提取到 {len(contacts)} 个联系人/群")
    
    # 自动复制
    root.clipboard_clear()
    root.clipboard_append(result_text)
    
    messagebox.showinfo("完成", f"✓ 提取到 {len(contacts)} 个联系人\n已自动复制到剪贴板")

def clear_extract():
    """清空提取区域"""
    extract_input.delete("1.0", tk.END)
    extract_output.delete("1.0", tk.END)
    extract_stats.config(text="")

def use_extracted_contacts():
    """将提取的联系人用到发送工具"""
    contacts = extract_output.get("1.0", tk.END).strip()
    if contacts:
        names_text.delete("1.0", tk.END)
        names_text.insert("1.0", contacts)
        notebook.select(1)  # 切换到发送标签
        messagebox.showinfo("提示", "已将联系人复制到发送工具")
    else:
        messagebox.showwarning("提示", "没有可使用的联系人")

# ==================== 批量发送功能 ====================
def start_send():
    global is_paused, is_running

    if is_running:
        log("【警告】已在运行中")
        return

    msg = msg_text.get("1.0", tk.END).strip()
    if not msg:
        log("【错误】内容不能为空")
        return

    # 获取联系人名称列表
    names_str = names_text.get("1.0", tk.END).strip()
    if not names_str:
        log("【错误】请输入联系人名称")
        return
    
    names = [name.strip() for name in names_str.split('\n') if name.strip()]
    if not names:
        log("【错误】联系人列表为空")
        return
    
    total = len(names)

    # 获取延时配置
    try:
        paste_delay = float(paste_delay_entry.get())
        send_delay = float(send_delay_entry.get())
        nav_delay = float(nav_delay_entry.get())
    except:
        log("【错误】延时配置必须是数字")
        return

    is_running = True
    is_paused = False
    btn_start.config(state=tk.DISABLED, text="运行中")

    log("=" * 50)
    log(f"发送人数：{total}")
    log(f"联系人列表：{names}")
    log(f"延时配置 - 粘贴:{paste_delay}s 发送:{send_delay}s 切换:{nav_delay}s")
    log("正在激活企业微信...")
    log("F4 暂停/继续 | ESC 紧急停止")
    log("=" * 50)

    try:
        # 使用快捷键激活企业微信
        pyautogui.hotkey('alt', 'shift', 's')
        time.sleep(0.6)
        log("✓ 已发送激活快捷键")

        for i in range(3, 0, -1):
            log(f"倒计时：{i}")
            time.sleep(1)

        # 核心逻辑：通过搜索用户名匹配联系人
        for i in range(total):
            if not is_running:
                log("\n⚠️ 已手动停止")
                break

            while is_paused:
                time.sleep(0.2)
                if not is_running:
                    break

            if not is_running:
                break

            current_name = names[i]
            log(f"\n→ 发送第 {i+1}/{total} 人：{current_name}")

            try:
                # 步骤1：搜索联系人
                log(f"  → 搜索：{current_name}")
                pyperclip.copy(current_name)
                time.sleep(0.1)
                
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.4)
                
                # 步骤2：打开聊天窗口
                pyautogui.press('enter')
                time.sleep(0.5)
                log(f"  ✓ 已打开与 {current_name} 的聊天")

                # 步骤3：发送消息
                pyperclip.copy(msg)
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(paste_delay)
                pyautogui.press('enter')
                time.sleep(send_delay)
                log(f"  ✓ 消息已发送")

            except Exception as e:
                log(f"【错误】发送第 {i+1} 人时出错: {str(e)}")
                log("提示：请确保企业微信窗口处于激活状态")
                break

        if is_running:
            log("\n🎉 全部发送完成！")
            time.sleep(0.5)
            pyautogui.press('esc')
            time.sleep(0.2)
            pyautogui.press('esc')
            time.sleep(0.3)
            log("✓ 已关闭企业微信")
        
    except Exception as e:
        log(f"【严重错误】{str(e)}")
    finally:
        is_running = False
        btn_start.config(state=tk.NORMAL, text="开始运行")

def stop_send():
    global is_running, is_paused
    if is_running:
        is_running = False
        is_paused = False
        log("\n【系统】正在停止...")

def start_thread():
    t = threading.Thread(target=start_send, daemon=False)
    t.start()

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    log(f"【系统】{'已暂停' if is_paused else '已继续'}")

# ==================== GUI ====================
root = tk.Tk()
root.title("企业微信批量发送工具 - 集成版")
root.geometry("900x800")

# 创建标签页
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=5, pady=5)

# ===== 标签1：联系人提取 =====
tab_extract = ttk.Frame(notebook)
notebook.add(tab_extract, text='📋 联系人提取')

ttk.Label(tab_extract, text="从 QQ/微信长截图中提取联系人", 
         font=("微软雅黑", 12, "bold")).pack(pady=10)

ttk.Label(tab_extract, text="步骤：1.长截图 2.识别文字 3.粘贴到下方 4.点击提取", 
         foreground="gray").pack(pady=5)

# 输入区域
ttk.Label(tab_extract, text="原始文本（粘贴在这里）").pack(anchor=tk.W, padx=20, pady=(10,5))
extract_input = scrolledtext.ScrolledText(tab_extract, width=110, height=12)
extract_input.pack(padx=20, pady=5)

# 按钮
extract_btn_frame = ttk.Frame(tab_extract)
extract_btn_frame.pack(pady=10)

ttk.Button(extract_btn_frame, text="🔧 提取联系人", command=extract_contacts, width=15).pack(side=tk.LEFT, padx=5)
ttk.Button(extract_btn_frame, text="📤 用到发送工具", command=use_extracted_contacts, width=15).pack(side=tk.LEFT, padx=5)
ttk.Button(extract_btn_frame, text="🗑️ 清空", command=clear_extract, width=15).pack(side=tk.LEFT, padx=5)

# 统计
extract_stats = ttk.Label(tab_extract, text="", font=("微软雅黑", 10), foreground="blue")
extract_stats.pack(pady=5)

# 输出区域
ttk.Label(tab_extract, text="提取结果（每行一个）").pack(anchor=tk.W, padx=20, pady=(10,5))
extract_output = scrolledtext.ScrolledText(tab_extract, width=110, height=15, wrap=tk.NONE)
extract_output.pack(padx=20, pady=5)

# ===== 标签2：批量发送 =====
tab_send = ttk.Frame(notebook)
notebook.add(tab_send, text='📤 批量发送')

ttk.Label(tab_send, text="企业微信批量发送工具", 
         font=("微软雅黑", 12, "bold")).pack(pady=10)

# 发送内容
ttk.Label(tab_send, text="发送内容").pack(anchor=tk.W, padx=20, pady=(10,0))
msg_text = scrolledtext.ScrolledText(tab_send, width=110, height=8)
msg_text.pack(padx=20, pady=5)
msg_text.insert("1.0", "你好，这是测试消息")

# 联系人
ttk.Label(tab_send, text="联系人名称（每行一个）").pack(anchor=tk.W, padx=20)
names_text = scrolledtext.ScrolledText(tab_send, width=110, height=10, wrap=tk.NONE)
names_text.pack(padx=20, pady=5)
names_text.insert("1.0", "张三\n李四")

# 延时配置
delay_frame = ttk.Frame(tab_send)
delay_frame.pack(fill=tk.X, padx=20, pady=5)

ttk.Label(delay_frame, text="延时配置(秒):").pack(side=tk.LEFT)
ttk.Label(delay_frame, text="粘贴后:").pack(side=tk.LEFT, padx=(10,2))
paste_delay_entry = ttk.Entry(delay_frame, width=6)
paste_delay_entry.pack(side=tk.LEFT)
paste_delay_entry.insert(0, "0.2")

ttk.Label(delay_frame, text="发送后:").pack(side=tk.LEFT, padx=(10,2))
send_delay_entry = ttk.Entry(delay_frame, width=6)
send_delay_entry.pack(side=tk.LEFT)
send_delay_entry.insert(0, "0.4")

ttk.Label(delay_frame, text="切换:").pack(side=tk.LEFT, padx=(10,2))
nav_delay_entry = ttk.Entry(delay_frame, width=6)
nav_delay_entry.pack(side=tk.LEFT)
nav_delay_entry.insert(0, "0.3")

# 按钮
send_btn_frame = ttk.Frame(tab_send)
send_btn_frame.pack(pady=8)

btn_start = ttk.Button(send_btn_frame, text="▶ 开始运行", command=start_thread)
btn_start.pack(side=tk.LEFT, padx=5)

btn_stop = ttk.Button(send_btn_frame, text="⏹ 停止", command=stop_send)
btn_stop.pack(side=tk.LEFT, padx=5)

# 日志
ttk.Label(tab_send, text="运行日志（F4 暂停/继续 | ESC 停止）").pack(anchor=tk.W, padx=20)
log_box = scrolledtext.ScrolledText(tab_send, width=110, height=12)
log_box.pack(padx=20, pady=5)

# 启动日志处理器
process_log_queue()

# 注册热键
keyboard.add_hotkey('f4', toggle_pause)
keyboard.add_hotkey('esc', stop_send)

# 窗口关闭事件
def on_closing():
    global is_running
    if is_running:
        if messagebox.askokcancel("退出", "正在运行中，确定要退出吗？"):
            is_running = False
            root.destroy()
    else:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
