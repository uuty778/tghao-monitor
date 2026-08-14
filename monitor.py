import json
import os
from datetime import datetime

print("开始运行监控...")

# 模拟订单数据（测试用，跑通后换成真实接口）
orders = [
    {
        "order_id": "TEST001",
        "goods_name": "测试商品",
        "amount": "99.00",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "contact": "测试联系方式",
        "_new": True
    }
]

# 写入 orders.json
with open('orders.json', 'w', encoding='utf-8') as f:
    json.dump(orders, f, ensure_ascii=False, indent=2)

print("已写入 orders.json，共", len(orders), "条订单")
print("完成！")
