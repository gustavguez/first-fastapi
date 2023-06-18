from fastapi import Depends
from typing import Annotated
from services.auth import validateAccessToken

oauth2Dependency = Annotated[dict, Depends(validateAccessToken)]
