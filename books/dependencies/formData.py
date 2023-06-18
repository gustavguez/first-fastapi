from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

formDataDependency = Annotated[OAuth2PasswordRequestForm, Depends()]
