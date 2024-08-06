"""
Module that contains authorization related classes and functions.
"""

from base64 import b64decode
from enum import Enum
from json import loads
from typing import Optional

from fastapi import Depends, Header
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from libs.exception import Unauthorized
from libs.response import ResponseCode

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

algorithm = "HS256"

unauthorized = Unauthorized(
    message="you are not authorized to access this endpoint",
    response_code=ResponseCode.UNAUTHORIZED,
    logstash_logging=False,
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def extract_user_info(
    token: Optional[str] = Header(default=None, alias="x-access-token")
):
    if token is None:
        return UserInfo(userId="", type=UserTypes.NONE)

    try:
        _, payload, _ = token.split(".")
        return UserInfo(**loads(b64decode(f"{payload}==")))
    except (ValueError, TypeError) as e:
        raise unauthorized from e


class UserInfo(BaseModel):
    user_id: str = Field(alias="userId")
    user_type: str = Field(alias="type")
    permissions: list[str] | None = None


class PermissionMatch(str, Enum):
    SOME = "SOME"
    ALL = "ALL"


class UserTypes(str, Enum):
    CUSTOMER = "CUSTOMER"
    OPERATIONS_USER = "OPERATIONS_USER"
    NONE = "NONE"
    BOTH = "BOTH"
    ALL = "ALL"


class EndpointACL:
    """
    Endpoint access control level management class for users.
    """

    def __init__(
        self,
        user_type: UserTypes = UserTypes.BOTH,
        permission_match_strategy: PermissionMatch = PermissionMatch.SOME,
        permissions: list[str] | None = None,
    ):
        self.user_type = user_type
        self.permissions = permissions
        self.permission_match_strategy = permission_match_strategy

    def __call__(self, user_info: UserInfo = Depends(extract_user_info)):
        if user_info.user_type == UserTypes.NONE:
            if self.user_type in [UserTypes.NONE, UserTypes.ALL]:
                return user_info
        elif user_info.user_type == UserTypes.CUSTOMER:
            if self.user_type in [
                UserTypes.CUSTOMER,
                UserTypes.BOTH,
                UserTypes.ALL,
            ]:
                return user_info

        elif user_info.user_type == UserTypes.OPERATIONS_USER:
            if self.user_type in [
                UserTypes.OPERATIONS_USER,
                UserTypes.BOTH,
                UserTypes.ALL,
            ]:
                if user_info.permissions is None:
                    raise unauthorized
                elif self.__is_user_permited(user_info.permissions):
                    return user_info

        raise unauthorized

    def __is_user_permited(self, user_perms: list[str]):
        if self.permissions is None:
            return True

        assert isinstance(self.permissions, list), "permissions must be a list"

        if self.permission_match_strategy == PermissionMatch.ALL:
            return sorted(self.permissions) == sorted(user_perms)
        return any(perm in self.permissions for perm in user_perms)
