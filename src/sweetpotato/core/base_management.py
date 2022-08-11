"""Provides base functionality for State and Props classes.

Todos:
    * Cleanup + add docstrings, typing
"""
import json
from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseManagement(ABC):
    """Interface for BaseProps & BaseState."""

    @property
    @abstractmethod
    def values(self):
        """Abstract property for state management key-value store."""
        raise NotImplementedError

    @abstractmethod
    def as_json(self) -> str:
        """Abstract as_json method."""
        return json.dumps(self.values)


class BaseState(BaseManagement):
    """Internal base class for state."""

    is_functional = False  #: Determines whether state object is contained in a functional component.

    def __init__(
        self,
        values: Optional[dict] = None,
    ) -> None:
        self._values = values if values else {}
        self.functions = []
        self.type = self.__class__.__name__.lower()

    @property
    def values(self) -> dict:
        """Property for state management key-value store."""
        return self._values

    def use_state(self, name: str = None, default_value: Any = None) -> tuple[str, str]:
        """Wrapper around React useState hook.

        Args:
            name: Name of state value.
            default_value: Default of state value.

        Returns:
            Tuple of values.

        Todos:
            * Add better docstring for this method.
        """
        state_output = f"set{name.title()}"
        state_function = f"this.setState({dict(name=name)});"
        self.functions.append(f"{state_output} = () => {state_function}")
        var = f"this.{state_output}", f"this.state.{name}"
        return var

    def as_json(self) -> str:
        """Return dict as json."""
        return super().as_json()


class BaseProps(BaseManagement):
    """Internal base class for props."""

    is_functional = (
        False  #: Determines whether prop object is contained in a functional component.
    )

    def __init__(self, state_obj: Optional[BaseState] = None) -> None:
        if state_obj:
            self.state = state_obj
            self._values = state_obj.values
        if not state_obj:
            self._values = {}
        self.type = self.__class__.__name__.lower()

    @property
    def values(self) -> dict:
        """Property for props management key-value store."""
        return self._values

    def as_json(self) -> str:
        """Return dict as json."""
        return super().as_json()
