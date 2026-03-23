from pydantic import BaseModel
from typing import Optional

class ApplicationProcess(BaseModel):
    status: int
    remark: Optional[str] = ""
