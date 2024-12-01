from fastapi import Depends, Request
from sqlmodel import Session, select
from config.database import get_session
from models.filestorage import CloudProvider


def load_cloud_providers(request: Request, session: Session = Depends(get_session)):
    request.state.providers = session.exec(select(CloudProvider)).all()