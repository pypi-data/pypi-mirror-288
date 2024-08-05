from typing import Callable, TypeAlias

from panflute import Element, Doc

Walker: TypeAlias = Callable[[Element, Doc | None], None]
