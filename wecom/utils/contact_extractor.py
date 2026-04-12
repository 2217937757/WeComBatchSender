"""
联系人提取工具
从粘贴的文本中提取联系人名称
"""
import re

def extract_contacts_from_text(raw_text):
    """
    从原始文本中提取联系人列表
    策略：通过正则匹配识别以字母开头的联系人名称行
    :param raw_text: 原始文本字符串
    :return: 去重后的联系人列表
    """
    if not raw_text or not raw_text.strip():
        return []
    
    lines = raw_text.split('\n')
    contacts = []
    seen_contacts = set()
    
    # 遍历所有行，通过模式匹配识别联系人
    for line in lines:
        line = line.strip()
        
        if not line:  # 跳过空行
            continue
        
        # 判断是否为联系人名称行
        if is_contact_name(line):
            # 清洗联系人名称
            cleaned = clean_contact_name(line)
            
            # 添加到结果（去重）
            if cleaned and cleaned not in seen_contacts:
                contacts.append(cleaned)
                seen_contacts.add(cleaned)
            
    return contacts


def is_contact_name(line):
    """
    判断一行文本是否为联系人名称
    规则：
    1. 以字母开头（通常是B）
    2. 包含数字和中文
    3. 长度适中（5-60字符）
    4. 不以标点符号开头
    
    :param line: 待判断的行
    :return: True 如果是联系人名称
    """
    if not line or len(line) < 5 or len(line) > 60:
        return False
    
    # 排除明显的非联系人行
    # 1. 以标点符号开头
    if line[0] in '.,;:!?\t':
        return False
    
    # 2. 纯标点或特殊字符
    if re.match(r'^[\.\-\*]+$', line):
        return False
    
    # 3. 常见的消息内容特征（以"在吗"、"你好"等开头）
    if re.match(r'^(在吗|你好|您好|请问|麻烦|谢谢)', line):
        return False
    
    # 4. 匹配联系人名称模式：以字母开头，包含数字和中文
    # 例如：B3.2韩静妇炎洁41@微信
    contact_pattern = r'^[A-Za-z][\d\.].*[\u4e00-\u9fff]'
    if re.search(contact_pattern, line):
        return True
    
    return False


def clean_contact_name(name):
    """
    清洗联系人名称
    规则：
    1. 移除末尾的 @微信 标记
    2. 移除末尾单独的 @ 符号
    3. 移除末尾的 @xxx 模式（如 @某人）
    4. 保留其他所有内容（包括数字、字母、中文、特殊符号等）
    
    :param name: 原始联系人名称
    :return: 清洗后的名称
    """
    if not name:
        return ""
    
    # 步骤1：移除末尾的 @微信
    cleaned = name.replace('@微信', '')
    
    # 步骤2：使用正则移除末尾的 @xxx 模式（@后面跟任意字符直到行尾）
    # 匹配末尾的 @ 及其后面的非空白字符
    cleaned = re.sub(r'@\S*$', '', cleaned)
    
    # 步骤3：去除首尾空白
    cleaned = cleaned.strip()
    
    return cleaned
