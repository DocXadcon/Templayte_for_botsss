from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


# @dataclass
# class DBConfig:
#     host: str
#     password: str
#     user: str
#     database: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    # db: DBConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS")
        ),
        misc=Miscellaneous()
    )

    #     db=DBConfig(
    #         host=env.str("DB_HOST"),
    #         password=env.str("DB_PASS"),
    #         user=env.st("DB_USER"),
    #         database=env.str("DB_NAME")
    #     ),
    #     misc=Miscellaneous()
    # )
