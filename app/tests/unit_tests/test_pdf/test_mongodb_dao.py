import pytest
from app.dao.mongodb_dao import MongoDBStorageDAO


@pytest.mark.asyncio
async def test_upload_download_file(mongodb):
    mongo_dao = MongoDBStorageDAO(mongodb)

    file_content = b"Example file content"
    filename = "test_file.pdf"

    file_id = await mongo_dao.upload_file(
        filename,
        file_content,
        metadata={
            "user_id": 1,
            "content_type": "1",
            "timestamp": "1",
        },
    )

    stream = await mongo_dao.download_file(file_id)
    downloaded_content = await stream.read()

    assert file_content == downloaded_content
