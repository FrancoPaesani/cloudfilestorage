from datetime import datetime
from typing import Optional

from fastapi import Cookie, Depends, HTTPException, Request
from sqlmodel import Session

from config.database import get_session
from models.auth import User
from services.auth import SessionService
from services.user import UserService


def validate_login(
    request: Request,
    session_cfs_tkn_ath: Optional[str] = Cookie(None),
    session: Session = Depends(get_session),
):
    if session_cfs_tkn_ath is None:
        raise HTTPException(status_code=403, detail="Invalid session")

    session_db = SessionService().get_session(session_cfs_tkn_ath, session)

    if session_db is None:
        raise HTTPException(status_code=403, detail="Invalid session")

    if datetime.now() > session_db.expires_date:
        raise HTTPException(status_code=403, detail="Session expired")

    user = UserService().get_user_from_session(session_cfs_tkn_ath, session)
    request.state.user = user
