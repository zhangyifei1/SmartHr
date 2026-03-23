from passlib.context import CryptContext
import sqlite3
import os

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
admin_password = "123456"  # 管理员密码，可自行修改
password_hash = pwd_context.hash(admin_password)

# 数据库路径
db_path = os.path.join(os.path.dirname(__file__), "database", "smarthr.db")

# 插入管理员用户
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 插入管理员用户
    cursor.execute("""
        INSERT INTO users (username, password_hash, user_type, status)
        VALUES (?, ?, ?, ?)
    """, ("admin", password_hash, 3, 1))

    admin_id = cursor.lastrowid
    print(f"管理员账号创建成功！")
    print(f"用户名: admin")
    print(f"密码: {admin_password}")
    print(f"用户ID: {admin_id}")

    conn.commit()
except sqlite3.IntegrityError:
    print("管理员账号 admin 已存在")
finally:
    conn.close()
