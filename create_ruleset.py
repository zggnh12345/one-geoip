import json
import os
import subprocess
from datetime import datetime

def run_command(command):
    """执行系统命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"命令执行失败: {command}")
            print(f"错误输出:\n{result.stdout}")
            return False
            
        print(f"执行成功: {command}")
        if result.stdout.strip():
            print(f"输出日志:\n{result.stdout}")
        return True
    except subprocess.TimeoutExpired:
        print(f"命令执行超时: {command}")
        return False
    except Exception as e:
        print(f"执行命令时发生意外错误: {str(e)}")
        return False

def create_and_push_ruleset():
    """创建规则集并推送到Git分支"""
    try:
        # ==================== 第一部分：生成规则集 ====================
        # 检查源文件存在性
        if not os.path.exists("china.txt"):
            print("错误: 未找到 china.txt 文件")
            return False
        
        # 读取IP列表
        ip_cidrs = []
        with open("china.txt", 'r') as f:
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line:
                    ip_cidrs.append(cleaned_line)
        
        # 构建JSON结构
        ruleset = {
            "version": 3,
            "rules": [{
                "ip_cidr": ip_cidrs
            }]
        }
        
        # 写入文件
        with open("one-china.json", 'w') as f:
            json.dump(ruleset, f, indent=4)
        print(f"成功生成规则集文件，包含 {len(ip_cidrs)} 条IP规则")

        # ==================== 第二部分：Git推送 ====================
        # 配置Git身份
        if not run_command('git config user.name "Ruleset Updater"'):
            return False
        if not run_command('git config user.email "updater@ruleset-generator"'):
            return False

        # 创建/重置分支
        if not run_command("git checkout --orphan rule-set"):
            print("尝试备选分支切换方式...")
            if not run_command("git checkout -B rule-set"):
                return False

        # 清理历史记录
        run_command("git rm -rf --cached .")  # 允许失败
        
        # 添加新文件
        if not run_command("git add -f one-china.json"):
            return False

        # 生成提交信息
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"自动更新中国IP规则集 {timestamp}"

        # 提交变更（允许空提交）
        if not run_command(f'git commit -m "{commit_msg}" --allow-empty'):
            print("提交可能为空，继续推送...")

        # 强制推送
        if not run_command("git push -f origin rule-set"):
            print("尝试备选推送方式...")
            return run_command("git push --set-upstream origin rule-set -f")

        print("规则集已成功更新并推送！")
        return True

    except Exception as e:
        print(f"处理过程中发生严重错误: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    if create_and_push_ruleset():
        sys.exit(0)
    else:
        sys.exit(1)
