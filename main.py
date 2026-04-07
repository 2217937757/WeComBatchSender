import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip
import time
import pyautogui
import threading
import keyboard
import queue
import sys

is_paused = False
is_running = False
log_queue = queue.Queue()  # 线程安全的日志队列

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    log(f"【系统】{'已暂停' if is_paused else '已继续'}")

def log(text):
    """线程安全的日志函数，将消息放入队列"""
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
    root.after(100, process_log_queue)  # 每100ms检查一次

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
    
    # 用换行符分割联系人名称，自动忽略空白行
    names = [name.strip() for name in names_str.split('\n') if name.strip()]
    if not names:
        log("【错误】联系人列表为空")
        return
    
    total = len(names)  # 自动根据联系人数量确定

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
            # 检查是否被停止
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
                
                # 聚焦搜索框并输入
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'a')  # 清空搜索框
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'v')  # 粘贴姓名
                time.sleep(0.4)  # 等待搜索结果
                
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
            # 完成后关闭企业微信
            time.sleep(0.5)
            pyautogui.press('esc')  # 从聊天窗口回到列表
            time.sleep(0.2)
            pyautogui.press('esc')  # 关闭企业微信
            time.sleep(0.3)
            log("✓ 已关闭企业微信")
        
    except Exception as e:
        log(f"【严重错误】{str(e)}")
    finally:
        is_running = False
        btn_start.config(state=tk.NORMAL, text="开始运行")

def stop_send():
    """紧急停止发送"""
    global is_running, is_paused
    if is_running:
        is_running = False
        is_paused = False
        log("\n【系统】正在停止...")

def start_thread():
    t = threading.Thread(target=start_send, daemon=False)  # 改为非daemon线程
    t.start()

# ==================== GUI ====================
root = tk.Tk()
root.title("企微批量发送工具")
root.geometry("700x780")

ttk.Label(root, text="发送内容").pack(anchor=tk.W, padx=10, pady=(8,0))
msg_text = scrolledtext.ScrolledText(root, width=90, height=10)
msg_text.pack(padx=10, pady=5)
msg_text.insert("1.0", "你好，这是测试消息")

ttk.Label(root, text="联系人名称（每行一个）").pack(anchor=tk.W, padx=10)
names_text = scrolledtext.ScrolledText(root, width=90, height=15, wrap=tk.NONE)
names_text.pack(padx=10, pady=5)
names_text.insert("1.0", "张三\n李四")

# 延时配置框架
delay_frame = ttk.Frame(root)
delay_frame.pack(fill=tk.X, padx=10, pady=5)

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

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=8)

btn_start = ttk.Button(btn_frame, text="开始运行", command=start_thread)
btn_start.pack(side=tk.LEFT, padx=5)

btn_stop = ttk.Button(btn_frame, text="停止", command=stop_send)
btn_stop.pack(side=tk.LEFT, padx=5)

ttk.Label(root, text="运行日志（F4 暂停/继续 | ESC 停止）").pack(anchor=tk.W, padx=10)
log_box = scrolledtext.ScrolledText(root, width=90, height=16)
log_box.pack(padx=10, pady=5)

# 启动日志队列处理器
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