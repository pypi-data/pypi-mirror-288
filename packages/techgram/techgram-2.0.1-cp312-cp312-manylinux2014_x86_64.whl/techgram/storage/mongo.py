# Ayiin - Xd
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinXd >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinXd/blob/main/LICENSE/>.
#
# FROM AyiinXd <https://github.com/AyiinXd/AyiinXd>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional


class MongoDB:
    mDb: AsyncIOMotorClient
    pyDb: MongoClient
    _pyMongo: Database
    _mongo: AsyncIOMotorDatabase
    def __init__(self, mongoUrl: Optional[str] = None, mongoName: Optional[str] = None):
        self._mongoUrl = mongoUrl
        self._mongoName = mongoName
        if self._mongoName is None:
            self._mongoName = "Techgram"
        if self._mongoUrl is not None:
            self.mDb = AsyncIOMotorClient(mongoUrl)
            self.pyDb = MongoClient(mongoUrl)
            self._pyMongo = self.pyDb[self._mongoName]
            self._mongo = self.mDb[self._mongoName]

    def collection(self, name: str) -> AsyncIOMotorCollection:
        return self._mongo[name]

    def pyCollection(self, name: str) -> Collection:
        return self._pyMongo[name]



db = MongoDB()
