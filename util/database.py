from motor import motor_asyncio
from constant.environ import MONGO_URL

client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["ticket_bot"]
ticket_counts = db["ticket_counts"]

ticket_count_cache: dict[int, int] = {}

async def cache_counts() -> None:
    async for count_data in ticket_counts.find():
        channel_id = count_data.get("channel_id")
        count = count_data.get("counts")
        ticket_count_cache[channel_id] = count

def get_counts(channel_id: int) -> int:
    return ticket_count_cache.get(channel_id) or 0

async def set_counts(channel_id: int, counts: int):
    query = {
        "channel_id": channel_id
    }
    value = {
        "channel_id": channel_id,
        "counts": counts
    }
    await ticket_counts.update_one(query, {"$set": value}, upsert=True)
    ticket_count_cache[channel_id] = counts

async def delete_counts(channel_id: int):
    result = await ticket_counts.delete_one({"channel_id": channel_id})
    if result.deleted_count > 0:
        ticket_count_cache.pop(channel_id, None)