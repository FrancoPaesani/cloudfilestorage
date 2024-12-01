from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException
from sqlmodel import Session, select

from config.utils import AUTH_JWT_KEY
from models.auth import User, UserSession
from schemas.auth import UserLogin, UserRegister
from services.user import UserService


class SessionService:
    def generate_jwt(self, user: str):
        expires_date = datetime.now(timezone.utc) + timedelta(hours=1)
        jwt_content = jwt.encode(
            {"user": user, "expires_date": expires_date.strftime("%Y%m%d % H:%M:%S")},
            key=AUTH_JWT_KEY,
            algorithm="HS256",
        )
        return (jwt_content, expires_date)

    def get_session(self, jwt_content: str, session: Session):
        session_db = session.exec(
            select(UserSession).where(UserSession.jwt == jwt_content)
        ).first()
        return session_db

    def save_session(self, user_session: UserSession, session: Session):
        session.add(user_session)
        session.commit()
        session.refresh(user_session)
        return user_session

    def delete_session(self, user_session: UserSession, session: Session):
        session.delete(user_session)


class HashService:
    def hash_password(self, password):
        key = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
        return key.decode()

    def validate_password(self, login_pwd, db_pwd):
        verification = bcrypt.checkpw(login_pwd.encode(), db_pwd.encode())

        return verification


class AuthService:
    def register_user(self, user: UserRegister, session: Session):
        user_db = User.model_validate(user)

        hashed_password = HashService().hash_password(user_db.password)
        user_db.password = hashed_password

        user_db = UserService().save_user(user_db, session)
        return user_db

    def authenticate_user(self, user: UserLogin, session: Session):
        user_db: User = UserService().get_user(user.user, session)

        if user_db is None:
            raise HTTPException(status_code=403, detail="Authentication failed")

        auth_valid = HashService().validate_password(user.password, user_db.password)

        if not (auth_valid):
            raise HTTPException(status_code=403, detail="Authentication failed")

        user_session_db = UserService().get_user_session(user_db.id, session)
        if user_session_db is not None:
            SessionService().delete_session(user_session_db, session)

        jwt_content, expires_date = SessionService().generate_jwt(user.user)

        user_session = UserSession(
            user_id=user_db.id, jwt=jwt_content, expires_date=expires_date
        )

        user_session = SessionService().save_session(user_session, session)

        return user_session
