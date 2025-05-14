import csv
import sqlite3

# 1) Открываем (или создаём) БД
conn = sqlite3.connect('gas_monitor/db.sqlite3')
cur = conn.cursor()

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

# 3) Читаем CSV и вставляем
with open('final_df.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    # Посмотрим, как называются колонки в файле
    print("CSV headers:", reader.fieldnames)

    rows = []
    for row in reader:
        # Замените 'DateTime' на точное имя из reader.fieldnames
        dt   = row['datetime']
        fact = float(row['gas_rate_fact'])
        plan = float(row['gas_rate_plan'])
        rows.append((dt, fact, plan))

# 4) Вставляем три поля в правильную таблицу
cur.executemany('''
    INSERT INTO chart_gasrecord (datetime, gas_rate_fact, gas_rate_plan)
    VALUES (?, ?, ?)
''', rows)

# 5) Сохраняем и закрываем
conn.commit()
conn.close()
