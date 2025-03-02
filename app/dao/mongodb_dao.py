from datetime import datetime
from typing import BinaryIO, Dict, Any
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId
from fastapi import HTTPException

class MongoDBStorageDAO:
    def __init__(self, db):
        self.db = db
        self.fs = AsyncIOMotorGridFSBucket(db)

    async def upload_file(
        self, 
        filename: str, 
        file: BinaryIO, 
        metadata: Dict[str, Any]
    ) -> str:
        try:
            file_id = await self.fs.upload_from_stream(
                filename,
                file,
                metadata=metadata
            )
            return str(file_id)
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload file: {str(e)}"
            )

    async def download_file(self, file_id: str):
        try:
            file_id = ObjectId(file_id)
            grid_out = await self.fs.open_download_stream(file_id)
            return grid_out
        except Exception as e:
            raise HTTPException(
                status_code=404, 
                detail=f"File not found: {str(e)}"
            )

    async def list_all_files(self):
        try:
            cursor = self.fs.find({})
            files = await cursor.to_list(length=None)
            return [self._convert_id_to_str(file) for file in files]
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to list files: {str(e)}"
            )

    async def list_user_files(self, user_id: int):
        try:
            cursor = self.fs.find({"metadata.user_id": user_id})
            files = await cursor.to_list(length=None)
            return [self._convert_id_to_str(file) for file in files]
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to list user files: {str(e)}"
            )

    @staticmethod
    def _convert_id_to_str(file: Dict) -> Dict:
        file["_id"] = str(file["_id"])
        return file
