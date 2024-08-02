# fastzdp_login
张大鹏开发fastapi专用于处理登录逻辑的模块框架

## 安装教程
```bash
pip install fastzdp_login
```

## 使用说明
基本用法
```python
import fastzdp_login
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine

# 创建数据库引擎
sqlite_url = "mysql+pymysql://root:zhangdapeng520@127.0.0.1:3306/zdppy_demo?charset=utf8mb4"
engine = create_engine(sqlite_url, echo=True)

# 确保表存在
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

app = FastAPI()

# 伪造一个密钥，实际使用时应该使用安全的方式存储
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 令牌有效期
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


app.include_router(fastzdp_login.get_user_router(
    get_db,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES * 60
))

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
```