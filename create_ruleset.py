import json
import os

def create_ruleset_json():
    """读取china.txt文件并创建sing-box规则集JSON文件"""
    try:
        # 检查china.txt是否存在
        if not os.path.exists("china.txt"):
            print("错误: china.txt 文件不存在")
            return False
        
        # 读取IP地址列表
        ip_cidrs = []
        with open("china.txt", 'r') as f:
            for line in f:
                # 去掉首尾空格
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
        return True
    
    except Exception as e:
        print(f"创建规则集JSON时出错: {e}")
        return False

if __name__ == "__main__":
    create_ruleset_json()
