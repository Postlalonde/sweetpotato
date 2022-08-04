"""
Todo:
    * Implement mixins for custom component.
"""
import json
from dataclasses import dataclass


@dataclass
class Prop:
    values: dict

    def as_json(self):
        """Return dict as json."""
        return json.dumps(self.values)


@dataclass
class State(Prop):
    pass


class CustomMixin:
    """Mixin methods for RootComponent"""
    extra_props: set = set()

    def __init__(self) -> None:
        if self.extra_props:
            # noinspection PyUnresolvedReferences
            self.props.update(self.extra_props)  # pylint: disable=no-attribute
