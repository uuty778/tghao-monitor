import requests
import json
import os

# 打印一条日志，确认脚本开始运行
print("="*50)
print("✅ monitor.py 脚本开始运行！")

# 获取环境变量（如果你之前没设置过，这里会打印 None，但不影响）
TGHAO_APPID = os.environ.get('TGHAO_APPID', '未设置')
TGHAO_CONTACTS = os.environ.get('TGHAO_CONTACTS', '未设置')
PUSHPLUS_TOKEN = os.environ.get('PUSHPLUS_TOKEN', '未设置')

print(f"🔧 环境变量 TGHAO_APPID: {TGHAO_APPID}")
print(f"🔧 环境变量 TGHAO_CONTACTS: {TGHAO_CONTACTS}")
print(f"🔧 环境变量 PUSHPLUS_TOKEN: {PUSHPLUS_TOKEN}")

def fetch_orders():
    """模拟抓取订单数据，实际项目中请替换为真实逻辑"""
    print("📥 正在模拟抓取订单数据...")
    orders = [
        {"id": "TEST_001", "status": "paid", "amount": 99.99, "time": "2025-09-08"},
        {"id": "TEST_002", "status": "shipped", "amount": 199.99, "time": "2025-09-07"}
    ]
    print(f"✅ 成功模拟抓取 {len(orders)} 条订单数据")
    return orders

def save_orders(orders):
    """保存订单数据到 orders.json"""
    print("💾 正在保存到 orders.json...")
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    print(f"✅ 已成功保存 {len(orders)} 条数据到 orders.json")

if __name__ == "__main__":
    print("="*50)
    print("🚀 开始执行监控任务...")
    try:
        orders = fetch_orders()
        save_orders(orders)
        print("🎉 监控任务执行完毕！")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        raise  # 抛出错误，让工作流标记为失败
    print("="*50)
