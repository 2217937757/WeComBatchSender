"""
每日动态密码生成器
支持两种模式：
1. 每日密码模式：每天生成一个6位数字密码
2. TOTP模式：每30秒刷新一次，前后30秒都有效（类似Google Authenticator）
"""
import datetime
import hashlib
import sys
import hmac
import struct
import time


# TOTP配置
TOTP_TIME_STEP = 30  # 时间步长（秒）
TOTP_DIGITS = 6      # 密码位数
TOTP_WINDOW = 1      # 允许的时间窗口（前后各1个窗口，共3个窗口）

# 密钥（用于TOTP，可以自定义）
# 注意：在实际应用中，这个密钥应该保密存储
SECRET_KEY = b'WeComBatchSender2024SecretKey'


def generate_daily_password(date=None):
    """
    根据日期生成每日密码（旧模式）
    
    Args:
        date: 可选的日期对象，默认为今天
        
    Returns:
        str: 6位数字密码
    """
    if date is None:
        date = datetime.date.today()
    
    # 使用日期作为种子生成密码
    date_str = date.strftime("%Y%m%d")
    
    # 使用SHA256哈希算法
    hash_object = hashlib.sha256(date_str.encode())
    hex_digest = hash_object.hexdigest()
    
    # 从哈希值中提取6位数字
    digits = [c for c in hex_digest if c.isdigit()]
    
    # 取前6位数字作为密码
    password = ''.join(digits[:6])
    
    # 如果不足6位，使用备用方案
    if len(password) < 6:
        # 使用日期的数字部分补充
        date_digits = date_str
        while len(password) < 6:
            idx = len(password) % len(date_digits)
            password += date_digits[idx]
    
    return password


def get_totp_token(secret=None, time_offset=0):
    """
    生成TOTP令牌（类似Google Authenticator）
    
    Args:
        secret: 密钥字节串，默认使用内置密钥
        time_offset: 时间偏移量（用于验证前后窗口）
        
    Returns:
        str: 6位数字TOTP令牌
    """
    if secret is None:
        secret = SECRET_KEY
    
    # 计算时间计数器（当前时间 / 时间步长）
    current_time = int(time.time()) // TOTP_TIME_STEP
    time_counter = current_time + time_offset
    
    # 将时间计数器转换为8字节大端序
    time_bytes = struct.pack('>Q', time_counter)
    
    # 使用HMAC-SHA1生成哈希
    hmac_hash = hmac.new(secret, time_bytes, hashlib.sha1).digest()
    
    # 动态截断
    offset = hmac_hash[-1] & 0x0F
    binary_code = (
        ((hmac_hash[offset] & 0x7f) << 24) |
        ((hmac_hash[offset + 1] & 0xff) << 16) |
        ((hmac_hash[offset + 2] & 0xff) << 8) |
        (hmac_hash[offset + 3] & 0xff)
    )
    
    # 生成指定位数的密码
    otp = binary_code % (10 ** TOTP_DIGITS)
    
    # 格式化为指定位数，不足补零
    return str(otp).zfill(TOTP_DIGITS)


def get_current_totp():
    """
    获取当前时间的TOTP令牌
    
    Returns:
        str: 6位数字TOTP令牌
    """
    return get_totp_token()


def verify_totp(user_token, secret=None):
    """
    验证用户输入的TOTP令牌
    允许前后各1个时间窗口的误差（共90秒有效期）
    
    Args:
        user_token: 用户输入的令牌
        secret: 密钥字节串
        
    Returns:
        bool: 验证是否通过
    """
    if secret is None:
        secret = SECRET_KEY
    
    # 验证当前窗口和前后的窗口
    for offset in range(-TOTP_WINDOW, TOTP_WINDOW + 1):
        expected_token = get_totp_token(secret, offset)
        if hmac.compare_digest(user_token, expected_token):
            return True
    
    return False


def get_totp_remaining_time():
    """
    获取当前TOTP令牌的剩余有效时间（秒）
    
    Returns:
        int: 剩余秒数
    """
    current_time = int(time.time())
    elapsed = current_time % TOTP_TIME_STEP
    remaining = TOTP_TIME_STEP - elapsed
    return remaining


def get_today_password():
    """
    获取今天的密码（保持向后兼容）
    现在返回TOTP令牌
    
    Returns:
        str: 6位数字密码（TOTP）
    """
    return get_current_totp()


def verify_password(input_password):
    """
    验证输入的密码是否正确（保持向后兼容）
    现在使用TOTP验证
    
    Args:
        input_password: 用户输入的密码
        
    Returns:
        bool: 密码是否正确
    """
    return verify_totp(input_password)


if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("🔐 TOTP 动态验证码生成器")
    print("="*60)
    print()
    
    # 显示当前TOTP
    current_totp = get_current_totp()
    remaining = get_totp_remaining_time()
    
    print(f"当前验证码: {current_totp}")
    print(f"剩余有效时间: {remaining} 秒")
    print()
    print("特性说明:")
    print("• 每30秒自动刷新一次")
    print("• 前后30秒内都有效（共90秒有效期）")
    print("• 类似 Google Authenticator")
    print()
    print("测试验证功能:")
    
    # 测试验证
    test_result = verify_password(current_totp)
    print(f"验证当前验证码: {'✓ 通过' if test_result else '✗ 失败'}")
    
    # 测试过期验证码
    old_totp = get_totp_token(time_offset=-2)
    test_old = verify_password(old_totp)
    print(f"验证过期验证码: {'✓ 通过' if test_old else '✗ 失败'}")
    
    print()
    print("="*60)
