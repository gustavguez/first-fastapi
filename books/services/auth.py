from datetime import timedelta, datetime
from passlib.context import CryptContext
from tablemodels.user import User
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated
from jose import jwt, JWTError
from starlette import status

JWT_SECRET = '0615c2ffeeeb07f3fda3fb1143bc1b9cae1327179aa803c32e6d3660b1921797'
JWT_ALGORITHM = 'HS256'

bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2Bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


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


async def validateAccessToken(token: Annotated[str, Depends(oauth2Bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        userEmail = payload.get('user')
        userId = payload.get('id')
        if userId is None or userEmail is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials!")
        return {'email': userEmail, 'id': userId}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials!")
