from constant.environ import BOT_OWNER_ID

def is_owner(user_id: int):
    return user_id == BOT_OWNER_ID