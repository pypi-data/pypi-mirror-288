from dataclasses import dataclass
from functools import cached_property
from re import compile, Pattern
from typing import Self

from panflute import Doc


@dataclass
class Config:
    """A config object."""

    labeled_only: bool = False
    r"""Only transform blocks when they contain a ``\label``."""

    eq_ref: str = r"\(eq:(?P<eq_id>[^)]+)\)"
    """What to match for, when looking for equation references. Must match an ``eq_id`` named group."""

    env_start: str = r"\begin{equation}"
    """Environment opening statement."""

    env_stop: str = r"\end{equation}"
    """Environment closing statement."""

    @cached_property
    def eq_ref_pattern(self) -> Pattern:
        """Pattern to match equation references. Determined by :attr:`eq_ref`."""
        return compile(self.eq_ref)

    @classmethod
    def from_doc(cls, doc: Doc | None) -> Self:
        """Load config from document metadata."""
        options = {}
        if doc is not None:
            data = doc.metadata.get("displaymath2equation", {})
            options = {k.replace("-", "_"): v for k, v in data.items()}

        return cls(**options)
