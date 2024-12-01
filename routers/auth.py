from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from config.database import get_session
from schemas.auth import UserLogin, UserRegister, UserResponse, UserSessionResponse
from services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register/", response_model=UserResponse)
def register(user: UserRegister, session: Session = Depends(get_session)):
    registered_user = AuthService().register_user(user, session)

    return registered_user


@auth_router.post("/authenticate/", response_model=UserSessionResponse)
def authenticate(
    response: Response, user: UserLogin, session: Session = Depends(get_session)
):
    user = UserLogin.model_validate(user)

    logged_user = AuthService().authenticate_user(user, session)

    response.set_cookie(
        "session_cfs_tkn_ath",
        logged_user.jwt,
        expires=logged_user.expires_date.strftime("%d/%m/%Y, %H:%M:%S"),
        httponly=True,
    )

    return logged_user
