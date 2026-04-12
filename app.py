"""
企业微信批量发送工具 - 集成版
包含：联系人提取 + 批量发送
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import pyperclip
import time
import pyautogui
import threading
import keyboard
import queue
import re
import os

# ==================== 全局变量 ====================
is_paused = False
is_running = False
log_queue = queue.Queue()
selected_images = []  # 存储选中的图片路径

# ==================== 日志系统 ====================
def log(text):
    """线程安全的日志函数，同时输出到界面和控制台"""
    # 输出到控制台
    print(text)
    # 输出到界面日志框
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
    seen_contacts = set()  # 用于去重
    
    # 遍历所有行，提取奇数行（第1、3、5...行，索引为0、2、4...）作为联系人
    for i in range(0, len(lines), 2):
        line = lines[i].strip()
        
        if not line:  # 跳过空行
            continue
        
        # 只去掉 @微信
        cleaned = line.replace('@微信', '').strip()
        
        # 添加到结果（去重）
        if cleaned and cleaned not in seen_contacts:
            contacts.append(cleaned)
            seen_contacts.add(cleaned)
    
    # 显示结果
    result_text = '\n'.join(contacts)
    extract_output.delete("1.0", tk.END)
    extract_output.insert("1.0", result_text)
    
    # 更新统计
    extract_stats.config(text=f"提取到 {len(contacts)} 个联系人/群（已去重）")
    
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

# ==================== 图片管理功能 ====================
def select_images():
    """选择多张图片"""
    global selected_images
    files = filedialog.askopenfilenames(
        title="选择图片",
        filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"), ("所有文件", "*.*")]
    )
    
    if files:
        selected_images.extend(files)
        update_image_list()
        log(f"✓ 已添加 {len(files)} 张图片")

def remove_selected_image():
    """移除选中的图片"""
    global selected_images
    selection = image_list.curselection()
    if selection:
        index = selection[0]
        removed = selected_images.pop(index)
        update_image_list()
        log(f"✓ 已移除: {os.path.basename(removed)}")

def clear_all_images():
    """清空所有图片"""
    global selected_images
    selected_images.clear()
    update_image_list()
    log("✓ 已清空所有图片")

def update_image_list():
    """更新图片列表显示"""
    image_list.delete(0, tk.END)
    for img_path in selected_images:
        filename = os.path.basename(img_path)
        image_list.insert(tk.END, f"📷 {filename}")

def copy_image_to_clipboard(image_path):
    """将图片复制到剪贴板（Windows）"""
    try:
        log(f"      [DEBUG] 开始复制图片: {image_path}")
        
        from PIL import Image
        import win32clipboard
        import win32con
        
        # 打开图片
        log(f"      [DEBUG] 正在打开图片...")
        img = Image.open(image_path)
        log(f"      [DEBUG] 图片尺寸: {img.size}, 模式: {img.mode}")
        
        # 转换为RGB模式（处理PNG透明度等问题）
        if img.mode != 'RGB':
            log(f"      [DEBUG] 转换图片模式: {img.mode} -> RGB")
            img = img.convert('RGB')
        
        # 保存到临时文件
        temp_path = os.path.join(os.environ.get('TEMP', '.'), 'wecom_temp_image.bmp')
        log(f"      [DEBUG] 保存临时文件: {temp_path}")
        img.save(temp_path, 'BMP')
        log(f"      [DEBUG] 临时文件大小: {os.path.getsize(temp_path)} bytes")
        
        # 读取BMP文件数据
        log(f"      [DEBUG] 读取BMP数据...")
        with open(temp_path, 'rb') as f:
            bmp_data = f.read()
        log(f"      [DEBUG] BMP数据大小: {len(bmp_data)} bytes")
        
        # 复制到剪贴板（使用DIB格式）
        log(f"      [DEBUG] 写入剪贴板...")
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, bmp_data[14:])  # 跳过BMP文件头
        win32clipboard.CloseClipboard()
        log(f"      [DEBUG] 成功写入剪贴板")
        
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
            log(f"      [DEBUG] 已清理临时文件")
            
        log(f"      [DEBUG] ✓ 图片复制成功")
        return True
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        log(f"      [DEBUG] ✗ 复制图片失败: {str(e)}")
        log(f"      [DEBUG] 错误详情:\n{error_detail}")
        return False

def prepare_message_with_images(msg, images):
    """
    准备包含文字和图片的消息
    策略：先粘贴文字，再依次粘贴图片，最后统一发送
    """
    try:
        log(f"    [DEBUG] 开始准备图文消息")
        log(f"    [DEBUG] 文字长度: {len(msg) if msg else 0}, 图片数量: {len(images)}")
        
        # 步骤1：粘贴文字内容
        if msg:
            log(f"    → 粘贴文字内容")
            pyperclip.copy(msg)
            time.sleep(0.2)
            log(f"    [DEBUG] 执行 Ctrl+V 粘贴文字")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            log(f"    [DEBUG] 文字粘贴完成")
        else:
            log(f"    [DEBUG] 无文字内容，跳过")
        
        # 步骤2：依次粘贴所有图片
        if images:
            log(f"    [DEBUG] 开始处理 {len(images)} 张图片")
            for img_idx, img_path in enumerate(images, 1):
                img_name = os.path.basename(img_path)
                log(f"    → 处理图片 [{img_idx}/{len(images)}]: {img_name}")
                log(f"    [DEBUG] 图片完整路径: {img_path}")
                log(f"    [DEBUG] 文件是否存在: {os.path.exists(img_path)}")
                
                # 复制图片到剪贴板
                log(f"    [DEBUG] 调用 copy_image_to_clipboard...")
                if copy_image_to_clipboard(img_path):
                    log(f"    [DEBUG] 等待 0.3 秒后粘贴")
                    time.sleep(0.3)
                    log(f"    [DEBUG] 执行 Ctrl+V 粘贴图片")
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.5)
                    log(f"    ✓ 图片已粘贴")
                else:
                    log(f"    ✗ 图片复制失败，跳过此图片")
        else:
            log(f"    [DEBUG] 无图片内容，跳过")
        
        # 步骤3：统一发送（按一次回车）
        log(f"    → 发送消息（按回车）")
        log(f"    [DEBUG] 执行 Enter 键")
        pyautogui.press('enter')
        time.sleep(1.0)
        log(f"    ✓ 消息已发送（包含文字+{len(images)}张图片）")
        
        return True
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        log(f"【错误】准备消息失败: {str(e)}")
        log(f"[DEBUG] 错误堆栈:\n{error_detail}")
        return False

# ==================== 批量发送功能 ====================
def start_send():
    global is_paused, is_running

    if is_running:
        log("【警告】已在运行中")
        return

    msg = msg_text.get("1.0", tk.END).strip()
    
    # 获取联系人名称列表
    names_str = names_text.get("1.0", tk.END).strip()
    if not names_str:
        log("【错误】请输入联系人名称")
        return
    
    names = [name.strip() for name in names_str.split('\n') if name.strip()]
    if not names:
        log("【错误】联系人列表为空")
        return
    
    # 自动检测发送内容
    send_text = bool(msg.strip()) if msg else False
    send_images = len(selected_images) > 0
    
    if not send_text and not send_images:
        log("【错误】请输入文字或选择图片")
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
    log(f"发送内容：{'文字' if send_text else ''} {'+图片' if send_images else ''}")
    if send_images:
        log(f"图片数量：{len(selected_images)}")
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

                # 步骤3：准备并发送消息（文字+图片在一条消息中）
                if send_text and send_images:
                    # 文字和图片一起发送
                    log(f"  → 准备图文消息")
                    prepare_message_with_images(msg, selected_images)
                    
                elif send_text:
                    # 只发送文字
                    log(f"  → 发送文字消息")
                    pyperclip.copy(msg)
                    time.sleep(0.1)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(paste_delay)
                    pyautogui.press('enter')
                    time.sleep(send_delay)
                    log(f"  ✓ 文字已发送")
                    
                elif send_images:
                    # 只发送图片（多张图片在一条消息中）
                    log(f"  → 准备图片消息（{len(selected_images)}张）")
                    prepare_message_with_images("", selected_images)

                log(f"  ✓ 第 {i+1} 人发送完成")

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
        btn_start.config(state=tk.NORMAL, text="▶ 开始运行")

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
root.geometry("900x850")

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

# 提示说明
ttk.Label(tab_send, text="💡 提示：程序会自动检测输入内容和已选图片", foreground="gray").pack(anchor=tk.W, padx=20, pady=(5,0))
ttk.Label(tab_send, text="   - 只输入文字 → 发送纯文字", foreground="gray").pack(anchor=tk.W, padx=20)
ttk.Label(tab_send, text="   - 只选择图片 → 发送纯图片", foreground="gray").pack(anchor=tk.W, padx=20)
ttk.Label(tab_send, text="   - 文字+图片 → 发送图文混合消息", foreground="gray").pack(anchor=tk.W, padx=20)

# 发送内容
ttk.Label(tab_send, text="发送内容").pack(anchor=tk.W, padx=20, pady=(10,0))
msg_text = scrolledtext.ScrolledText(tab_send, width=110, height=6)
msg_text.pack(padx=20, pady=5)
msg_text.insert("1.0", "你好，这是测试消息")

# 图片选择区域
img_select_frame = ttk.Frame(tab_send)
img_select_frame.pack(fill=tk.X, padx=20, pady=5)

ttk.Button(img_select_frame, text="📁 选择图片", command=select_images, width=12).pack(side=tk.LEFT, padx=2)
ttk.Button(img_select_frame, text="❌ 移除选中", command=remove_selected_image, width=12).pack(side=tk.LEFT, padx=2)
ttk.Button(img_select_frame, text="🗑️ 清空全部", command=clear_all_images, width=12).pack(side=tk.LEFT, padx=2)

# 图片列表
ttk.Label(tab_send, text="已选图片列表").pack(anchor=tk.W, padx=20, pady=(5,0))
image_list = tk.Listbox(tab_send, width=108, height=4)
image_list.pack(padx=20, pady=5)

# 联系人
ttk.Label(tab_send, text="联系人名称（每行一个）").pack(anchor=tk.W, padx=20)
names_text = scrolledtext.ScrolledText(tab_send, width=110, height=8, wrap=tk.NONE)
names_text.pack(padx=20, pady=5)
names_text.insert("1.0", "小刀\n开发测试用")

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
