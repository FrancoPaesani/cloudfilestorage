from sqlmodel import Session, select

from models.auth import User, UserSession
from models.filestorage import CloudProvider, UserFiles, UserStorage
from schemas.filestorage import FileInfo


class UserService:
    def get_user(self, username: str, session: Session) -> User:
        user_db = session.exec(select(User).where(User.user == username)).first()
        return user_db

    def save_user(self, user: User, session: Session):
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def get_user_session(self, id: int, session: Session) -> User:
        user_session_db = session.exec(
            select(UserSession).where(UserSession.user_id == id)
        ).first()
        return user_session_db

    def get_user_from_session(self, jwt_content: str, session: Session) -> User:
        user_session_db, user_db = session.exec(
            select(UserSession, User).where(User.id == UserSession.user_id and UserSession.jwt == jwt_content)
        ).first()
        return user_db


class UserStorageService:
    def get_storage_per_user(self, session: Session):
        return session.exec(select(UserStorage, CloudProvider).where(UserStorage.cloud_provider_id == CloudProvider.id)).all()

    def save_user_file_metadata(
        self, user_file: UserFiles, session: Session
    ) -> UserFiles:
        session.add(user_file)
        session.commit()

        return user_file

    def file_exists(self, file: FileInfo, session: Session) -> FileInfo:
        result = session.exec(
            select(UserFiles).where(
                UserFiles.file_name == file.file_name
                and UserFiles.file_path == file.file_path
            )
        ).all()

        return len(result) > 0
