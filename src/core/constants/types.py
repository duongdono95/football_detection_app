from typing import TypedDict, Literal, List, Optional, Union

class JerseyObjectType(TypedDict):
    id: int
    bbox: tuple[int, int, int, int]
    confidence: float
    class_id: int
    name: int


class DetectedObjectType(TypedDict):
    id: int
    class_id: int
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
    jerseys: Optional[List[JerseyObjectType]]
