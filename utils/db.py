from models import User


async def get_user(user_id: int) -> User:
    return await User.find_one(User.user_id == user_id)


async def add_user_wb(user_id: int, wb_jwt: str):
    return await User(user_id=user_id, wb_jwt=wb_jwt, market='wb').insert()


async def add_user_ya(user_id: int, ya_token: str, ya_id: int):
    return await User(user_id=user_id, ya_token=ya_token, ya_id=ya_id, market='ya').insert()
