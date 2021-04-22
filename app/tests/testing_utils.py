import asyncio


def perform(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return wrapper


@perform
async def do_find_one(collection, query):
    document = await collection.find_one(query)
    return document


@perform
async def do_insert_one(collection, data):
    document = await collection.insert_one(data)
    return document
