from typing import Dict, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field

from classiq.interface.ide.visual_model import OperationLevel


class FunctionDebugInfo(BaseModel):
    name: str
    parameters: Dict[str, Union[int, float, None]]
    level: OperationLevel
    is_allocate_or_free: bool = Field(default=False)


class DebugInfoCollection(BaseModel):
    # Pydantic only started supporting UUID as keys in Pydantic V2
    # See https://github.com/pydantic/pydantic/issues/2096#issuecomment-814860206
    # For now, we use strings as keys in the raw data and use UUID in the wrapper logic
    data: Dict[str, FunctionDebugInfo] = Field(default_factory=dict)

    def __setitem__(self, key: UUID, value: FunctionDebugInfo) -> None:
        self.data[str(key)] = value

    def get(self, key: UUID) -> Optional[FunctionDebugInfo]:
        return self.data.get(str(key))

    def __getitem__(self, key: UUID) -> FunctionDebugInfo:
        return self.data[str(key)]

    def __contains__(self, key: UUID) -> bool:
        return str(key) in self.data
