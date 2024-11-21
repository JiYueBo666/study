import sys
import os

# 获取项目根目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # backend 目录
sys.path.append(project_root)

from app.models.database import engine
from app.models.article import Article
from app.models.user import User


def migrate():
    print("开始迁移...")
    try:
        # 删除现有表（谨慎使用！）
        Article.__table__.drop(engine, checkfirst=True)
        print("旧表删除成功")

        # 重新创建表
        Article.__table__.create(engine)
        print("新表创建成功")
    except Exception as e:
        print(f"迁移出错: {str(e)}")
        raise


if __name__ == "__main__":
    migrate()
    print("迁移完成！")
