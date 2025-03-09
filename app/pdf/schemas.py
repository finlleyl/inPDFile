from pydantic import BaseModel


class SPdf(BaseModel):
    pass


class SUploadOut(BaseModel):
    file_id: str
    document_id: int
    status: str


class SHistoryOut(BaseModel):
    file_name: str
    file_size: str
    file_path: str
    status: str
    classification: str
    document_type: str
    upload_date: str
    has_signature: str
    has_stamp: str
