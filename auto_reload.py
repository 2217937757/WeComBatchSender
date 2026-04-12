"""
自动重载管理器
监控主程序运行时间，12小时后自动重启
"""
import sys
import os
import time
import subprocess
import threading
from datetime import datetime, timedelta


class AutoReloadManager:
    def __init__(self, main_script="app.py", reload_hours=12):
        """
        初始化自动重载管理器
        
        Args:
            main_script: 主程序脚本路径
            reload_hours: 重载间隔（小时），默认12小时
        """
        self.main_script = main_script
        self.reload_hours = reload_hours
        self.reload_seconds = reload_hours * 3600  # 转换为秒
        self.start_time = None
        self.process = None
        self.running = False
        
    def start_main_program(self):
        """启动主程序"""
        print(f"\n{'='*60}")
        print(f"🚀 正在启动主程序: {self.main_script}")
        print(f"⏰ 自动重载时间: {self.reload_hours} 小时后")
        print(f"{'='*60}\n")
        
        try:
            # 启动主程序进程
            self.process = subprocess.Popen(
                [sys.executable, self.main_script],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            self.start_time = time.time()
            self.running = True
            return True
        except Exception as e:
            print(f"❌ 启动主程序失败: {e}")
            return False
    
    def stop_main_program(self):
        """停止主程序"""
        if self.process and self.process.poll() is None:
            print("\n⏹️  正在停止主程序...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            print("✓ 主程序已停止")
    
    def get_elapsed_time(self):
        """获取已运行时间"""
        if not self.start_time:
            return 0
        return time.time() - self.start_time
    
    def format_time(self, seconds):
        """格式化时间显示"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def monitor_and_reload(self):
        """监控并自动重载"""
        print("\n" + "="*60)
        print("🔄 自动重载管理器已启动")
        print("="*60)
        
        while self.running:
            elapsed = self.get_elapsed_time()
            remaining = self.reload_seconds - elapsed
            
            if remaining <= 0:
                # 时间到，执行重载
                print("\n" + "!"*60)
                print("⏰ 已达到重载时间！正在重启主程序...")
                print("!"*60)
                
                # 停止当前进程
                self.stop_main_program()
                
                # 等待一下确保进程完全停止
                time.sleep(2)
                
                # 重新启动
                if not self.start_main_program():
                    print("❌ 重启失败，退出管理器")
                    break
                
                # 重置计时器
                continue
            
            # 显示倒计时（每30秒更新一次）
            if int(elapsed) % 30 == 0 or remaining < 60:
                elapsed_str = self.format_time(elapsed)
                remaining_str = self.format_time(remaining)
                print(f"\r⏱️  已运行: {elapsed_str} | 距离下次重载: {remaining_str}", end="", flush=True)
            
            # 检查主程序是否意外退出
            if self.process and self.process.poll() is not None:
                print("\n\n⚠️  主程序意外退出")
                choice = input("是否重新启动？(y/n): ").strip().lower()
                if choice == 'y':
                    if not self.start_main_program():
                        break
                else:
                    break
            
            time.sleep(1)
    
    def run(self):
        """运行自动重载管理器"""
        # 首次启动主程序
        if not self.start_main_program():
            return
        
        try:
            # 开始监控
            self.monitor_and_reload()
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断，正在关闭...")
        finally:
            # 清理资源
            self.stop_main_program()
            self.running = False
            print("\n✓ 自动重载管理器已退出")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🔧 企业微信批量发送工具 - 自动重载管理器")
    print("="*60)
    
    # 配置参数
    RELOAD_HOURS = 12  # 12小时后重载
    
    print(f"\n📋 配置信息:")
    print(f"   • 主程序: app.py")
    print(f"   • 重载间隔: {RELOAD_HOURS} 小时")
    print(f"   • 启动方式: 自动管理")
    
    # 创建并运行管理器
    manager = AutoReloadManager(
        main_script="app.py",
        reload_hours=RELOAD_HOURS
    )
    
    manager.run()


if __name__ == "__main__":
    main()
