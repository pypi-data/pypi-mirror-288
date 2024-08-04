import logging
from abc import ABC, abstractmethod
from typing import Annotated, Any, get_type_hints

from kaya_module_sdk.src.utils.constraints.minimum import kmin
from kaya_module_sdk.src.utils.metadata.display_description import \
    DisplayDescription
from kaya_module_sdk.src.utils.metadata.display_name import DisplayName
from kaya_module_sdk.src.utils.metadata.minimum import Min

log = logging.getLogger(__name__)


class Args(ABC):
    _length: Annotated[
        int,
        DisplayName("Length"),
        DisplayDescription("Number of elements used from given data set."),
        Min(1),
    ]
    _errors: Annotated[
        list,
        DisplayName("Errors"),
        DisplayDescription("Collection of things that went very, very wrong."),
    ]

    @property
    def errors(self) -> None:
        return self._errors

    @property
    def length(self) -> int:
        return self._length[0]

    def set_errors(self, *values: Any) -> None:
        self._errors += list(values)

    @kmin(1)
    def set_length(self, value: int) -> None:
        assert isinstance(value, int)
        self._length = [value]

    def metadata(self):
        return get_type_hints(self, include_extras=True)
