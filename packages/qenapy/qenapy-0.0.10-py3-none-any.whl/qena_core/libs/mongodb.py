from asyncio import get_event_loop
from dataclasses import dataclass
from typing import List

from bson.objectid import ObjectId
from motor.core import AgnosticClient, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel

from qena_core.libs.logger import get_logger
from qena_core.settings import settings

client: AgnosticClient = AsyncIOMotorClient(settings.connection_string)
client.get_io_loop = get_event_loop

db: AgnosticDatabase = client[settings.db]


class MongoDBManager:
    @staticmethod
    async def start():
        server_info = await client.server_info()

        if server_info["ok"] != 1.0:
            raise RuntimeError("mongodb is not healthy")

        get_logger().info(
            'Connection opened to mongodb server\t"mongodb://%s:%s/%s"',
            client.HOST,
            client.PORT,
            settings.db,
        )

    @staticmethod
    def stop():
        client.close()


class MongoDBObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


@dataclass
class CollectionIndexes:
    collection: str
    indexes: List[IndexModel]


async def create_indexes(collections_indexes_pair: List[CollectionIndexes]):
    """
    Create indexes for specified collections.
    :param list collections_indexes_pair: list of collection and their indexes.
    """
    for collection_indexes in collections_indexes_pair:
        await db[collection_indexes.collection].create_indexes(
            collection_indexes.indexes
        )


async def drop_indexes(collections_indexes_pair: List[CollectionIndexes]):
    """
    Drop indexes for specified collections.
    :param list collections_indexes_pair: list of collection and their indexes.
    """
    for collection_indexes in collections_indexes_pair:
        await db[collection_indexes.collection].drop_indexes()


def transactional(func):
    async def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return await func(*args, **kwargs)

        async with await client.start_session() as session:
            async with session.start_transaction():
                kwargs["session"] = session

                return await func(*args, **kwargs)

    return wrapper
