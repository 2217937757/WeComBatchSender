"""
联系人名单整理工具
配合 QQ/微信 长截图使用，快速整理联系人名单
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re

def clean_text():
    """清理粘贴的文本，提取联系人姓名"""
    raw_text = input_text.get("1.0", tk.END)
    
    if not raw_text.strip():
        messagebox.showwarning("提示", "请先粘贴文本")
        return
    
    # 分割成行
    lines = raw_text.split('\n')
    
    contacts = []
    # 匹配各种时间/日期格式
    time_patterns = [
        r'^\d{1,2}:\d{2}',           # 14:30 或 9:30
        r'^昨天\d{1,2}:\d{2}',        # 昨天18:33
        r'^星期[一二三四五六日天]',    # 星期六、星期四
        r'^\d{2}/\d{2}',              # 03/18、03/08
        r'^\d+分钟前',                 # 24分钟前、5分钟前
        r'^\d+小时前',                 # 2小时前、1小时前
        r'^昨天',                      # 昨天
        r'^前天',                      # 前天
    ]
    
    def is_timestamp(line):
        """检查是否是时间戳行"""
        for pattern in time_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    for i in range(len(lines)):
        line = lines[i].strip()
        
        # 检查当前行是否是时间戳
        if is_timestamp(line):
            # 如果是时间戳，取上两行作为联系人名称（企业微信布局）
            if i >= 2:
                contact_line = lines[i - 2].strip()  # 上两行是联系人
                if contact_line:  # 不为空
                    # 清理多余符号
                    contact_line = contact_line.replace('@微信', '').replace('@...', '').replace('@', '')
                    contact_line = contact_line.strip()  # 去除首尾空格
                    if contact_line:  # 清理后不为空
                        contacts.append(contact_line)
    
    # 显示结果（保持原始顺序）
    result_text = '\n'.join(contacts)
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", result_text)
    
    # 更新统计
    stats_label.config(text=f"提取到 {len(contacts)} 个联系人/群")
    
    # 自动复制到剪贴板
    root.clipboard_clear()
    root.clipboard_append(result_text)
    
    messagebox.showinfo("完成", f"✓ 提取到 {len(contacts)} 个联系人/群\n已自动复制到剪贴板")

def clear_all():
    """清空所有内容"""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    stats_label.config(text="")

def copy_output():
    """复制结果到剪贴板"""
    result = output_text.get("1.0", tk.END).strip()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        messagebox.showinfo("提示", "已复制到剪贴板")
    else:
        messagebox.showwarning("提示", "没有可复制的内容")

# ==================== GUI ====================
root = tk.Tk()
root.title("联系人名单整理工具")
root.geometry("800x700")

# 标题
title_label = ttk.Label(root, text="📋 联系人名单整理工具", font=("微软雅黑", 14, "bold"))
title_label.pack(pady=10)

# 使用说明
instruction = ttk.Label(root, text="使用方法：1.从QQ/微信长截图中复制文字  2.粘贴到下方  3.点击整理\n提示：会自动提取时间戳上两行的联系人/群名（企业微信布局）", 
                       foreground="gray")
instruction.pack(pady=5)

# 输入区域
ttk.Label(root, text="原始文本（粘贴在这里）").pack(anchor=tk.W, padx=20, pady=(10,5))
input_text = scrolledtext.ScrolledText(root, width=100, height=12)
input_text.pack(padx=20, pady=5)

# 按钮区域
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

btn_clean = ttk.Button(btn_frame, text="🔧 整理提取", command=clean_text, width=15)
btn_clean.pack(side=tk.LEFT, padx=5)

btn_copy = ttk.Button(btn_frame, text="📋 复制结果", command=copy_output, width=15)
btn_copy.pack(side=tk.LEFT, padx=5)

btn_clear = ttk.Button(btn_frame, text="🗑️ 清空", command=clear_all, width=15)
btn_clear.pack(side=tk.LEFT, padx=5)

# 统计信息
stats_label = ttk.Label(root, text="", font=("微软雅黑", 10), foreground="blue")
stats_label.pack(pady=5)

# 输出区域
ttk.Label(root, text="整理结果（每行一个姓名）").pack(anchor=tk.W, padx=20, pady=(10,5))
output_text = scrolledtext.ScrolledText(root, width=100, height=15, wrap=tk.NONE)
output_text.pack(padx=20, pady=5)

# 底部提示
tip_label = ttk.Label(root, text="💡 提示：整理完成后可以直接粘贴到批量发送工具中使用", 
                     foreground="green", font=("微软雅黑", 9))
tip_label.pack(pady=10)

root.mainloop()
