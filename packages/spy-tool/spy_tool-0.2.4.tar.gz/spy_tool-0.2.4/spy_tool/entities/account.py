import random
from dataclasses import dataclass
from dynaconf import LazySettings
from typing_extensions import Self


@dataclass
class Account(object):
    """
    usage:
        settings.toml
        [default.account.baidu.user1]
        owner = "xxx"
        username = "123456"
        password = "888888"

        [default.account.360.user1]
        owner = "yyy"
        username = "654321"
        password = "000000"

    """
    platform: str
    owner: str
    username: str
    password: str

    @classmethod
    def get_random_account(cls, platform: str, settings: LazySettings) -> Self:
        users = settings.account[platform]
        user = users[random.choice(list(users.keys()))]
        return cls(
            platform=platform,
            owner=user.owner,
            username=user.username,
            password=user.password
        )
