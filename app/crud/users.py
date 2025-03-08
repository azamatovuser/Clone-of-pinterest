from app.models.users import User as UserDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    def __init__(self, db):
        self.db = db

    def get_user(self, username):
        user = self.db.query(UserDB).filter(UserDB.username == username).first()
        return user
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def register(self, user_request, hashed_password):
        new_user = UserDB(
            username=user_request.username,
            full_name=user_request.full_name,
            hashed_password=hashed_password,
        )
        self.db.add(new_user)
        self.db.commit()