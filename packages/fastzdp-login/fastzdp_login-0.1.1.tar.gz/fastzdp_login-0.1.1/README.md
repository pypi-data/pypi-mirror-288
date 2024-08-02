# fastzdp_login

#### 介绍
张大鹏开发fastapi专用于处理登录逻辑的模块框架

#### 软件架构
软件架构说明


#### 安装教程
```bash
pip install fastzdp_login
```

#### 使用说明
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

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
