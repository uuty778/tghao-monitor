import os
import requests
import json
import time
from datetime import datetime

APPID = os.environ.get('TGHAO_APPID', '你的appid')
CONTACTS = os.environ.get('TGHAO_CONTACTS', '138xxxx,139xxxx')
PUSHPLUS = os.environ.get('PUSHPLUS_TOKEN', '')
STATE_FILE = 'state.json'
ORDERS_FILE = 'orders.json'

def load_seen():
    try:
        with open(STATE_FILE, 'r') as f:
            return set(json.load(f).get('ids', []))
    except:
        return set()

def save_seen(ids):
    with open(STATE_FILE, 'w') as f:
        json.dump({'ids': list(ids)}, f)

def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def query(contact):
    try:
        r = requests.get('https://tghao.com/', params={
            'c': 'api', 'act': 'query_order',
            'appid': APPID, 'contact': contact
        }, timeout=15)
        print(f'[{datetime.now()}] {contact} -> {r.status_code}')
        j = r.json()
        if isinstance(j, dict):
            return j.get('data', [])
        return []
    except Exception as e:
        print(f'query error: {e}')
        return []

def push(title, content):
    if not PUSHPLUS:
        return
    try:
        requests.post('https://www.pushplus.plus/send', json={
            'token': PUSHPLUS, 'title': title,
            'content': content, 'template': 'txt'
        })
    except:
        pass

seen = load_seen()
orders = load_orders()
print(f'loaded {len(seen)} known ids, {len(orders)} orders')

for contact in CONTACTS.split(','):
    contact = contact.strip()
    if not contact:
        continue
    for o in query(contact):
        oid = str(o.get('order_id') or o.get('order_sn') or o.get('id', ''))
        if oid and oid not in seen:
            seen.add(oid)
            o['_new'] = True
            o['_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            orders.insert(0, o)
            msg = f"联系方式: {contact}\n商品: {o.get('goods_name', o.get('product', ''))}\n金额: ¥{o.get('amount', o.get('price', ''))}\n时间: {o.get('_time', '')}"
            print(f'NEW: {msg}')
            push('TGHAO 新订单', msg)

save_seen(seen)
save_orders(orders)
print('done')
