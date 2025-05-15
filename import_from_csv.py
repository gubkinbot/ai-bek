import csv
import sqlite3
from datetime import datetime

# 1) Открываем (или создаём) БД
conn = sqlite3.connect('gas_monitor/db.sqlite3')
cur  = conn.cursor()

# 2) Создаём таблицу (если ещё нет)
cur.execute('''
CREATE TABLE IF NOT EXISTS chart_gasrecord (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime         TEXT    NOT NULL,
    gas_rate_fact    REAL    NOT NULL,
    gas_rate_plan    REAL    NOT NULL,
    gas_rate_v1      REAL,
    gas_rate_v2      REAL,
    gas_rate_v3      REAL
);
''')

# 3) Очищаем таблицу перед новой загрузкой
cur.execute('DELETE FROM chart_gasrecord')

# 4) Функция-конвертер для чисел вида "0,00" или ""
def to_float(s):
    if not s:
        return 0.0
    s = s.strip().replace(',', '.')
    return float(s)

rows = []
with open('final_df.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    print("CSV headers:", reader.fieldnames)

    # запомним, если есть лишний пустой ключ
    extra = '' if '' in reader.fieldnames else None

    for row in reader:
        raw_dt = row.get('datetime', '').strip()
        # парсим оба варианта даты
        try:
            dt_obj = datetime.fromisoformat(raw_dt)
        except ValueError:
            dt_obj = datetime.strptime(raw_dt, "%d.%m.%Y %H:%M")
        iso_dt = dt_obj.isoformat()

        fact = to_float(row.get('gas_rate_fact', ''))
        plan = to_float(row.get('gas_rate_plan', ''))
        v1   = to_float(row.get('gas_rate_v1',    ''))
        v2   = to_float(row.get('gas_rate_v2',    ''))
        v3   = to_float(row.get('gas_rate_v3',    ''))

        rows.append((iso_dt, fact, plan, v1, v2, v3))

# 5) Вставляем все поля в таблицу
cur.executemany('''
    INSERT INTO chart_gasrecord
      (datetime, gas_rate_fact, gas_rate_plan, gas_rate_v1, gas_rate_v2, gas_rate_v3)
    VALUES (?, ?, ?, ?, ?, ?)
''', rows)

# 6) Сохраняем и закрываем
conn.commit()
conn.close()
