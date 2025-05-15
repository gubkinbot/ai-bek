import csv
import sqlite3
from datetime import datetime

# 1) Открываем (или создаём) БД
conn = sqlite3.connect('gas_monitor/db.sqlite3')
cur = conn.cursor()

# 2) Создаём таблицу (если ещё нет)
cur.execute('''
CREATE TABLE IF NOT EXISTS chart_gasrecord (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime             NOT NULL,
    gas_rate_fact    REAL    NOT NULL,
    gas_rate_plan    REAL    NOT NULL,
    gas_rate_v1      REAL,
    gas_rate_v2      REAL,
    gas_rate_v3      REAL
);
''')

# 3) Очищаем таблицу перед новой загрузкой
cur.execute('DELETE FROM chart_gasrecord')

# 4) Читаем CSV и готовим данные
with open('final_df.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    print("CSV headers:", reader.fieldnames)

    rows = []
    for row in reader:
        # Исходная строка даты, например "08.03.2025 0:00"
        raw_dt = row['datetime']  
        # Парсим в datetime и сразу переводим в ISO 8601
        dt_obj   = datetime.strptime(raw_dt, "%d.%m.%Y %H:%M")
        iso_dt   = dt_obj.isoformat()

        fact = float(row['gas_rate_fact'])
        plan = float(row['gas_rate_plan'])
        v1   = float(row.get('gas_rate_v1', 0) or 0)
        v2   = float(row.get('gas_rate_v2', 0) or 0)
        v3   = float(row.get('gas_rate_v3', 0) or 0)

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
