"""Provides React state management capacity for sweetpotato components.

React hooks may be accessed from the State class.

Todos:
    * Cleanup + add docstrings, typing
"""
import json
from typing import Optional, Any

from sweetpotato.core.base_management import BaseProps, BaseState


class State(BaseState):
    """Public class representation of React state.

    Examples:
        `state = State({'isAuthenticated': False})`
    """

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
        if self.is_functional:
            state_output = f"const [{name}, set{name.title()}]"
            state_function = f"React.useState({json.dumps(default_value)});"
            self.functions.append(f"{state_output} = {state_function}")
            var = f"set{name.title()}", name
            return var
        return super().use_state(name, default_value)

    def use_effect(
        self, name: str = None, default_value: Any = None
    ) -> tuple[str, str]:
        """Wrapper around React useEffect hook.

        Args:
            name: Name of state value.
            default_value: Default of state value.

        Returns:
            Tuple of values.

        Todos:
            * Add better docstring for this method.
        """
        raise NotImplementedError

    def __getitem__(self, item: Any):
        return self.values[item]


class Props(BaseProps):
    """Public class representation of React props.

    Expected value is a state object.

    Examples:
        `props = Props(state)`
    """

    def __init__(self, values: Optional[State] = None) -> None:
        super().__init__(values)

    def __getitem__(self, item: Any):
        if self.state.is_functional:
            return f"props.{item}"
        return f"this.props.{item}"
