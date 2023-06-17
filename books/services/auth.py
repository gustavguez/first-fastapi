from datetime import timedelta, datetime
from passlib.context import CryptContext
from tablemodels.user import User
from jose import jwt

JWT_SECRET = '0615c2ffeeeb07f3fda3fb1143bc1b9cae1327179aa803c32e6d3660b1921797'
JWT_ALGORITHM = 'HS256'

bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hashPassword(password: str):
    return bcryptContext.hash(password)


def findValidUser(username: str, password: str, db):
    user = db.query(User).filter(User.email == username).first()
    if not user or not bcryptContext.verify(password, user.password):
        return False
    return user


def createAccessToken(email: str, userId: int, expires_delta: timedelta):
    encode = {'id': userId, 'user': email}
    expires = datetime.utcnow() + expires_delta
    encode.update({'expires': str(expires)})
    return jwt.encode(encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
