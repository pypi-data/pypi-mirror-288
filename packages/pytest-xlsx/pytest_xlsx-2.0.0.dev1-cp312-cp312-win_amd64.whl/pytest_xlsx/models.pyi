from pydantic import BaseModel

class Case(BaseModel):
    id: int
    meta: dict[str, list[list[str]]]
    steps: list[dict]
    @property
    def name(self) -> str: ...
    @property
    def mark(self) -> list: ...
    @property
    def vars(self): ...

class Suite(BaseModel):
    name: str
    case_list: list[Case]
    def __call__(self, *args, **kwargs) -> None: ...
