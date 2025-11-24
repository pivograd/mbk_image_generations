from typing import Any, Dict, Optional
from pydantic import BaseModel, HttpUrl


class GenerateImageRequest(BaseModel):
    image_url: HttpUrl
    mode: str = "base"
    extra_text: Optional[str] = None


class GenerateImageResponse(BaseModel):
    result: Dict[str, Any]
