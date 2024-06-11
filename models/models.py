from typing import Optional

from beanie import Document, Indexed


class User(Document):
    user_id: Indexed(int, unique=True)
    ya_token: Optional[str] = None
    ya_id:  Optional[int] = 0
    wb_jwt: Optional[str] = None
