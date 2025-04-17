import json
import os
import subprocess

def create_ruleset_json():
    """读取china.txt文件并创建sing-box规则集JSON文件，并推送到指定分支"""
    try:
        # 检查china.txt是否存在
        if not os.path.exists("china.txt"):
            print("错误: china.txt 文件不存在")
            return False
        
        # 读取IP地址列表
        ip_cidrs = []
        with open("china.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    ip_cidrs.append(line)
        
        # 创建规则集JSON结构
        ruleset = {
            "version": 3,
            "rules": [
                {
                    "ip_cidr": ip_cidrs
                }
            ]
        }
        
        # 保存到文件
        with open("one-china.json", 'w') as f:
            json.dump(ruleset, f, indent=4)
        
        print(f"已创建规则集JSON文件: one-china.json，包含 {len(ip_cidrs)} 条IP规则")

        # 执行Git推送命令
        push_commands = [
            'git config --global user.name "GitHub Actions"',
            'git config --global user.email "actions@github.com"',
            'git add one-china.json',
            'git commit -m "Auto-update China ruleset"',
            'git push origin HEAD:rule-set --force'
        ]
        
        for cmd in push_commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"命令执行失败: {cmd}")
                print("错误输出:", result.stderr)
                return False
        
        print("已成功推送到 rule-set 分支")
        return True

    except Exception as e:
        print(f"处理过程中出错: {e}")
        return False

if __name__ == "__main__":
    create_ruleset_json()
