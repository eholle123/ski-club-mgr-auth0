from authorization_header_elements import get_bearer_token
from fastapi import Depends, Request
from json_web_token import JsonWebToken
from sqlalchemy.engine.base import Engine


def validate_token(token: str = Depends(get_bearer_token)):
    return JsonWebToken(token).validate()

# dependency function for database engine
def get_engine(request: Request) -> Engine:
    return request.app.state.engine