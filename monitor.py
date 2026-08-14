import os, requests, json, time
from datetime import datetime

APPID = os.environ['TGHAO_APPID']
CONTACTS = os.environ['TGHAO_CONTACTS'].split(',')
PUSHPLUS = os.environ.get('PUSHPLUS_TOKEN', '')
STATE_FILE = 'state.json'
ORDERS_FILE = 'orders.json'

def load_seen():
    try: return set(json.load(open(STATE_FILE)).get('ids', []))
    except: return set()

def save_seen(s):
    json.dump({'ids': list(s)}, open(STATE_FILE, 'w'))

def load_orders():
    try: return json.load(open(ORDERS_FILE))
    except: return []

def save_orders(o):
    json.dump(o, open(ORDERS_FILE, 'w'), ensure_ascii=False, indent=2)

def query(c):
    try:
        r = requests.get('https://tghao.com/', params={'c':'api','act':'query_order','appid':APPID,'contact':c}, timeout=15)
        j = r.json()
        return j.get('data', []) if isinstance(j, dict) else []
    except Exception as e:
        print('err', e); return []

def push(t, c):
    if PUSHPLUS:
        requests.post('https://www.pushplus.plus/send', json={'token':PUSHPLUS,'title':t,'content':c,'template':'txt'})

seen = load_seen()
orders = load_orders()
for c in CONTACTS:
    c = c.strip()
    if not c: continue
    for o in query(c):
        oid = str(o.get('order_id') or o.get('order_sn') or o.get('id',''))
        if oid and oid not in seen:
            seen.add(oid)
            o['_new'] = True
            o['_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            o['contact'] = c
            orders.insert(0, o)
            push('TGHAO 新订单', f"联系方式:{c}\n商品:{o.get('goods_name',o.get('product',''))}\n金额:¥{o.get('amount',o.get('price',''))}")
print('found', len(orders), 'orders total')
save_seen(seen)
save_orders(orders)
