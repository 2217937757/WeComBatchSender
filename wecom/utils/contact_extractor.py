"""
联系人提取工具
从粘贴的文本中提取联系人名称
"""

def extract_contacts_from_text(raw_text):
    """
    从原始文本中提取联系人列表
    :param raw_text: 原始文本字符串
    :return: 去重后的联系人列表
    """
    if not raw_text or not raw_text.strip():
        return []
    
    lines = raw_text.split('\n')
    contacts = []
    seen_contacts = set()
    
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
            
    return contacts
