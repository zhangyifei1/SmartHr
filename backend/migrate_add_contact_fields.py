#!/usr/bin/env python3
"""
数据库迁移脚本 - 为企业表添加联系人字段
执行方法: python migrate_add_contact_fields.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from sqlalchemy import text


def check_column_exists(table_name: str, column_name: str) -> bool:
    """检查列是否已存在"""
    with engine.connect() as conn:
        # SQLite 获取表信息的方式
        result = conn.execute(text(f"PRAGMA table_info({table_name})"))
        columns = [row[1] for row in result]
        return column_name in columns


def add_column(table_name: str, column_def: str):
    """添加列"""
    column_name = column_def.split()[0]
    if check_column_exists(table_name, column_name):
        print(f"列 {column_name} 已存在，跳过")
        return

    sql = f"ALTER TABLE {table_name} ADD COLUMN {column_def}"
    print(f"执行: {sql}")
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print(f"列 {column_name} 添加成功")


def main():
    print("开始执行数据库迁移...")
    print(f"数据库连接: {engine.url}")

    try:
        # 添加联系人字段
        add_column("enterprise_profiles", "contact_name VARCHAR(50)")
        add_column("enterprise_profiles", "contact_phone VARCHAR(20)")
        add_column("enterprise_profiles", "contact_email VARCHAR(100)")

        print("\n迁移完成！")
        return 0
    except Exception as e:
        print(f"\n迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
