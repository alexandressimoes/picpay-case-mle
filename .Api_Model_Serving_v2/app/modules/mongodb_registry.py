from __future__ import annotations

from datetime import datetime
from typing import Any

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


class MongoRegistryManager:
    """Centralizes the persistence of model metadata and transaction records in MongoDB."""

    def __init__(
        self,
        mongodb_uri: str,
        db_name: str = "picpay_metadata",
        models_collection: str = "model_registry",
        transactions_collection: str = "transactions_registry",
    ) -> None:
        self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[db_name]
        self.models_col: Collection = self.db[models_collection]
        self.transactions_col: Collection = self.db[transactions_collection]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self.models_col.create_index([("model_name", ASCENDING)], unique=True)
        self.models_col.create_index([("is_active", ASCENDING)])
        self.models_col.create_index([("last_used_at", DESCENDING)])

        self.transactions_col.create_index([("timestamp", DESCENDING)])
        self.transactions_col.create_index([("model_name", ASCENDING), ("timestamp", DESCENDING)])

    def ping(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except PyMongoError:
            return False

    def upsert_and_activate_model(self, model_name: str) -> None:
        now = datetime.utcnow()

        # Desativa qualquer modelo ativo anterior.
        self.models_col.update_many(
            {"model_name": {"$ne": model_name}, "is_active": True, "deleted": {"$ne": True}},
            {"$set": {"is_active": False}},
        )

        self.models_col.update_one(
            {"model_name": model_name},
            {
                "$setOnInsert": {
                    "downloaded_at": now,
                },
                "$set": {
                    "last_used_at": now,
                    "is_active": True,
                    "deleted": False,
                },
            },
            upsert=True,
        )

    def remove_model(self, model_name: str) -> bool:
        now = datetime.utcnow()
        result = self.models_col.update_one(
            {"model_name": model_name, "deleted": {"$ne": True}},
            {
                "$set": {
                    "deleted": True,
                    "is_active": False,
                    "deleted_at": now,
                }
            },
        )
        return result.modified_count > 0

    def model_exists(self, model_name: str) -> bool:
        return (
            self.models_col.find_one(
                {"model_name": model_name, "deleted": {"$ne": True}},
                {"_id": 1},
            )
            is not None
        )

    def get_last_used_model(self) -> str | None:
        model = self.models_col.find_one(
            {"is_active": True, "deleted": {"$ne": True}},
            {"_id": 0, "model_name": 1},
            sort=[("last_used_at", DESCENDING)],
        )
        if model:
            return model["model_name"]

        fallback = self.models_col.find_one(
            {"deleted": {"$ne": True}},
            {"_id": 0, "model_name": 1},
            sort=[("last_used_at", DESCENDING)],
        )
        return fallback["model_name"] if fallback else None

    def get_model_registry(self) -> dict[str, Any]:
        downloaded = [
            item["model_name"]
            for item in self.models_col.find(
                {"deleted": {"$ne": True}},
                {"_id": 0, "model_name": 1},
                sort=[("model_name", ASCENDING)],
            )
        ]

        return {
            "downloaded_models": downloaded,
            "last_used_model": self.get_last_used_model(),
        }

    def save_prediction(self, payload: dict[str, Any]) -> None:
        document = {
            "input": payload["input"],
            "output": payload["output"],
            "model_name": payload["model_name"],
            "timestamp": payload["timestamp"],
            "created_at": datetime.utcnow(),
        }
        self.transactions_col.insert_one(document)

    def list_predictions(self) -> list[dict[str, Any]]:
        docs = list(
            self.transactions_col.find(
                {},
                {"_id": 0, "input": 1, "output": 1, "model_name": 1, "timestamp": 1},
                sort=[("timestamp", ASCENDING)],
            )
        )
        return docs
