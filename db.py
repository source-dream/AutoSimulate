'''
数据库实现模块
'''

import sqlite3
import json
from log import logger

def open_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn: sqlite3.Connection) -> None:
    conn.commit()
    conn.close()

# 创建表和索引
def create_table() -> None:
    conn, cursor = open_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,            -- 自增数字主键
            alpha TEXT,                                      -- 字典作为 JSON 字符串存储
            alpha_id TEXT,                                   -- 文本类型
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 时间类型，默认当前时间
            simulate_id TEXT                                 -- 文本类型
        )          
    ''')
    close_db(conn)

def init_db() -> None:
    create_table()

def add_record_memory(alpha, alpha_id, simulate_id) -> None:
    conn, cursor = open_db()
    if isinstance(alpha, dict):
        alpha = json.dumps(alpha)
    cursor.execute(
        'INSERT INTO record (alpha, alpha_id, simulate_id) VALUES (?, ?, ?)',
        (alpha, alpha_id, simulate_id)
    )
    logger.info(f"已保存记录: {alpha_id}")
    close_db(conn)

def is_record_exist(field: str, value) -> bool:
    """
    判断指定字段中是否存在特定值。
    
    参数：
        field (str): 要查询的字段名，例如 'id', 'alpha', 'alpha_id'。
        value: 要查询的值。
    
    返回：
        bool: 如果存在匹配的记录，返回 True，否则返回 False。
    """
    conn, cursor = open_db()
    if isinstance(value, dict):
        value = json.dumps(value)
    query = f'SELECT 1 FROM record WHERE {field} = ?'
    cursor.execute(query, (value,))
    is_exist = cursor.fetchone() is not None
    close_db(conn)
    return is_exist

init_db()