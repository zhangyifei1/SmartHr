from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        # 检查管理员是否已存在
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("管理员账号已存在")
            return

        # 创建管理员
        admin = User(
            username="admin",
            email="admin@smarthr.com",
            phone="13800138000",
            password=get_password_hash("admin123456"),
            user_type=3,  # 管理员
            status=1
        )
        db.add(admin)
        db.commit()
        print("管理员账号创建成功")
        print("账号: admin")
        print("密码: admin123456")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
