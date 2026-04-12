"""
每日密码生成器 - 独立运行脚本
运行此脚本可获取今天的6位数字验证码
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wecom.utils.daily_password import get_today_password


def main():
    """显示今天的密码"""
    from wecom.utils.daily_password import get_current_totp, get_totp_remaining_time
    
    password = get_current_totp()
    remaining = get_totp_remaining_time()
    
    print("=" * 50)
    print("🔐 企业微信批量发送工具 - TOTP动态验证码")
    print("=" * 50)
    print()
    print(f"当前验证码: {password}")
    print(f"剩余有效时间: {remaining} 秒")
    print()
    print("使用说明:")
    print("1. 复制上面的6位数字验证码")
    print("2. 打开企业微信批量发送工具")
    print("3. 在验证对话框中输入验证码")
    print("4. 点击'验证'按钮即可使用软件")
    print()
    print("特性说明:")
    print("- 验证码每30秒自动刷新")
    print("- 前后30秒内都有效（共90秒）")
    print("- 类似 Google Authenticator")
    print("=" * 50)
    

if __name__ == "__main__":
    main()
