import requests
import json
import os

# 这里是你之前可能设置过的密钥，如果没设置过可以先留空或者随便填个测试值
TGHAO_APPID = os.environ.get('TGHAO_APPID', '')
TGHAO_CONTACTS = os.environ.get('TGHAO_CONTACTS', '')
PUSHPLUS_TOKEN = os.environ.get('PUSHPLUS_TOKEN', '')

def fetch_orders():
    # 这里是模拟抓取数据的逻辑，实际你需要替换成你原来的代码
    # 为了测试，我们先返回一个假数据，确保流程能跑通
    orders = [
        {"id": "12345", "status": "paid", "amount": 100},
        {"id": "67890", "status": "shipped", "amount": 200}
    ]
    return orders

def save_orders(orders):
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(orders)} 条订单数据到 orders.json")

if __name__ == "__main__":
    print("开始运行监控...")
    orders = fetch_orders()
    save_orders(orders)
    print("监控运行完成！")
