import time
from fastapi import APIRouter, status, Body, Depends, HTTPException
from sqlalchemy.orm import Session as SASession
from sqlmodel import select
from .jwt_util import get_jwt
from .passlib_util import hash_256, verify_256
from .user_model import User


def get_user_router(
        get_db,
        jwt_key="zhangdapeng520",
        jwt_algorithm="HS256",
        jwt_token_expired=3 * 60 * 60,
):
    user_router = APIRouter()

    @user_router.post("/register", status_code=status.HTTP_201_CREATED)
    def register_user(
            username: str = Body(str, min_length=2, max_length=36),
            password: str = Body(str, min_length=6, max_length=128),
            db: SASession = Depends(get_db),
    ):
        # 检查用户名是否已存在
        user = db.exec(select(User).where(User.username == username)).first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        # 创建新用户
        new_user = User(username=username, password=hash_256(password))
        db.add(new_user)
        try:
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operation failed")

        return {"message": "User registered successfully", "user_id": new_user.id}

    # 登录接口
    @user_router.post("/login", status_code=status.HTTP_200_OK)
    async def login_for_access_token(
            username: str = Body(str, min_length=2, max_length=36),
            password: str = Body(str, min_length=6, max_length=128),
            db: SASession = Depends(get_db),
    ):
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
        if not verify_256(password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
        data = {"username": user.username, "id": user.id, "time": time.time(),
                "expired": jwt_token_expired}
        access_token = get_jwt(data, jwt_key, jwt_algorithm)
        return {"access_token": access_token, "token_type": "bearer"}

    return user_router
