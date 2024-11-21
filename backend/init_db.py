import sys
import os

# 获取项目根目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.models.database import init_db
from app.models import article, user  # 确保导入所有模型

if __name__ == "__main__":
    try:
        init_db()
        print("数据库表创建成功！")
    except Exception as e:
        print(f"初始化数据库失败: {str(e)}")
        raise
