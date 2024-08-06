import pytest
from . import settings as settings
from .fixtures import getfixtureinfo as getfixtureinfo
from .funcs import LoadData as LoadData
from .templates import item_locals as item_locals, render as render
from _pytest.fixtures import FuncFixtureInfo as FuncFixtureInfo
from _pytest.python import CallSpec2 as CallSpec2, FunctionDefinition, Metafunc
from _typeshed import Incomplete
from collections.abc import Generator
from pytest_xlsx import funcs as funcs, models as models
from typing import Any, Iterable, Mapping

logger: Incomplete

class XlsxFile(pytest.Module):
    obj: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def collect(self) -> Generator[Incomplete, None, None]: ...

class XlsxSheet(pytest.Class):
    xlsx_data: models.Suite
    obj: models.Suite
    @classmethod
    def from_parent(cls, parent, *, name, obj: Incomplete | None = None, **kw): ...
    def collect(self) -> Iterable[pytest.Item | pytest.Collector]: ...

class XlsxItem(pytest.Function):
    xlsx_data: models.Case
    max_step_no: int
    current_step_no: int
    current_step: dict
    usefixtures: dict
    obj: Incomplete
    originalname: Incomplete
    callspec: Incomplete
    fixturenames: Incomplete
    def __init__(self, name: str, parent, case: models.Case, own_markers: list | None = None, config: pytest.Config | None = None, callspec: CallSpec2 | None = None, callobj=..., keywords: Mapping[str, Any] | None = None, session: pytest.Session | None = None, fixtureinfo: FuncFixtureInfo | None = None, originalname: str | None = None) -> None: ...
    @property
    def cls(self): ...
    @property
    def is_first_step(self): ...
    @property
    def is_last_step(self): ...
    @property
    def location(self): ...
    @classmethod
    def from_parent(cls, parent, name, case: models.Case, **kw): ...
    def runtest(self) -> None: ...
    def repr_failure(self, excinfo): ...

class XlsxItemDefinition(FunctionDefinition, XlsxItem): ...
class XlsxMetafunc(Metafunc): ...
