"""
Todo:
    * Implement mixins for custom component.
"""
import json
from typing import Optional


class BaseProps:
    def __init__(self, values: Optional[dict] = None):
        self.values = values if values else {}
        self.type = self.__class__.__name__.lower()

    def as_json(self):
        """Return dict as json."""
        return json.dumps(self.values)


class BaseState(BaseProps):
    pass


class CustomMixin:
    """Mixin methods for RootComponent"""

    extra_props: set = set()

    def __init__(self) -> None:
        if self.extra_props:
            # noinspection PyUnresolvedReferences
            self.props.update(self.extra_props)  # pylint: disable=no-attribute
