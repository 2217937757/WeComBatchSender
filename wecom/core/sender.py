"""
企业微信发送核心逻辑
包含图片处理和消息发送功能
"""
import os
import time
import pyautogui
import pyperclip

def copy_image_to_clipboard(image_path, log_callback=None):
    """将图片复制到剪贴板（Windows）"""
    def _log(text):
        if log_callback:
            log_callback(text)
            
    try:
        from PIL import Image
        import win32clipboard
        import win32con
        
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        temp_path = os.path.join(os.environ.get('TEMP', '.'), 'wecom_temp_image.bmp')
        img.save(temp_path, 'BMP')
        
        with open(temp_path, 'rb') as f:
            bmp_data = f.read()
        
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, bmp_data[14:])
        win32clipboard.CloseClipboard()
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return True
    except Exception as e:
        _log(f"复制图片失败: {str(e)}")
        return False

def prepare_message_with_images(msg, images, log_callback=None):
    """
    准备包含文字和图片的消息
    策略：先依次粘贴图片，再粘贴文字，最后统一发送
    """
    def _log(text):
        if log_callback:
            log_callback(text)

    try:
        # 步骤1：依次粘贴所有图片
        if images:
            for img_idx, img_path in enumerate(images, 1):
                if copy_image_to_clipboard(img_path, log_callback):
                    time.sleep(0.3)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.5)
                else:
                    _log(f"✗ 图片复制失败: {os.path.basename(img_path)}")
        
        # 步骤2：粘贴文字内容
        if msg:
            pyperclip.copy(msg)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
        
        # 步骤3：统一发送
        pyautogui.press('enter')
        time.sleep(1.0)
        
        return True
    except Exception as e:
        _log(f"【错误】准备消息失败: {str(e)}")
        return False

def send_to_contact(name, msg, images, delays, log_callback=None, stop_check=None):
    """
    向指定联系人发送消息
    :param name: 联系人名称
    :param msg: 文字消息
    :param images: 图片路径列表
    :param delays: 延时配置字典 {'paste': 0.2, 'send': 0.4, 'nav': 0.3}
    :param log_callback: 日志回调函数
    :param stop_check: 停止检查回调函数，返回 True 表示应停止
    """
    def _log(text):
        if log_callback:
            log_callback(text)

    if stop_check and stop_check():
        return False

    try:
        _log(f"  → 搜索：{name}")
        pyperclip.copy(name)
        time.sleep(0.1)
        
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.4)
        
        pyautogui.press('enter')
        time.sleep(0.5)
        
        if msg and images:
            prepare_message_with_images(msg, images, log_callback)
        elif msg:
            pyperclip.copy(msg)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(delays['paste'])
            pyautogui.press('enter')
            time.sleep(delays['send'])
        elif images:
            prepare_message_with_images("", images, log_callback)
            
        _log(f"  ✓ 已发送给 {name}")
        return True
    except Exception as e:
        _log(f"【错误】发送给 {name} 时出错: {str(e)}")
        return False
