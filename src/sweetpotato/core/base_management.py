"""Provides base functionality for State and Props classes.

Todos:
    * Cleanup + add docstrings, typing
"""
import json
from abc import abstractmethod
from typing import Optional, Protocol, Union, Any

import sweetpotato.core.js_utils as js_utils


class _ProtocolFunction(Protocol):
    """Protocol interface for Function."""

    value: str
    name: str
    type: str


class Function(_ProtocolFunction):
    """Public class representation of .js functions."""

    def __init__(self, value: str, name: str, is_functional: bool) -> None:
        self.value = value
        self.name = name
        self.type = "" if is_functional else js_utils.add_this()

    def __repr__(self) -> str:
        return f"() => {self.type}{self.name}({self.value})"

    # def __call__(self, *args, **kwargs):
    #     print(args, kwargs)


class _ProtocolState(Protocol):
    """Protocol interface for State."""

    type: str
    functions: list[str]
    values: Optional[dict[str, Any]]
    is_functional: bool

    @abstractmethod
    def use_state(
        self,
        name: str,
        increment: Optional[Union[int, str]] = None,
        decrement: Optional[Union[int, str]] = None,
    ) -> tuple[Function, str]:
        """Protocol method wrapper around React useState hook."""
        ...

    @abstractmethod
    def use_effect(
        self, name: str, default_value: Optional[Any] = None
    ) -> tuple[str, str]:
        """Wrapper around React useEffect hook.

        Args:
            name: Name of state value.
            default_value: Default of state value.

        Returns:
            Tuple of values.

        See Also:
            https://reactjs.org/docs/hooks-effect.html

        Todos:
            * Add better docstring for this method.
        """
        ...

    @abstractmethod
    def _set_class_state(
        self, name: str, incr_or_decr_val: str
    ) -> tuple[Function, str]:
        """Protocol method sets state in class format."""
        ...

    @abstractmethod
    def _set_functional_state(
        self, name: str, default_value: Any, incr_or_decr_val: str
    ) -> tuple[Function, str]:
        """Protocol method sets state in functional format."""
        ...

    @abstractmethod
    def as_json(self) -> str:
        """Protocol method for json rendering."""
        ...


class _ProtocolProps(Protocol):
    """Protocol interface for Props."""

    type: str
    state: _ProtocolState
    values: dict

    @abstractmethod
    def as_json(self) -> str:
        """Protocol method for json rendering."""
        ...


class State(_ProtocolState):
    """Public class representation of React state.

    The State class allows for dynamic data within application (button title value changes, etc.)
    components. State is accessed within a respective component; to be accessed in an external component,
    a Prop instance with the state object as an argument must be passed to the external component.

    Examples:
        `state = State({"isAuthenticated": False})`
        `set_pressed, pressed = state.use_state(name="pressed", default_value=False)`

    Todos:
        * Implement State.use_effect (React.useEffect) method.
        * Add increment and decrement operations.
    """

    is_functional = False  #: Determines whether state object is contained in a functional component.

    def __init__(
        self,
        values: Optional[dict[str, Any]] = None,
    ) -> None:
        self.values = values if values else {}
        self.functions = []
        self.type = self.__class__.__name__.lower()

    def as_json(self) -> str:
        """Return dict as json."""
        return json.dumps(self.values)

    def use_state(
        self,
        name: str,
        increment: Optional[Union[int, str]] = None,
        decrement: Optional[Union[int, str]] = None,
    ) -> tuple[Function, str]:
        """Wrapper around React useState hook.

        Args:
            name: Name of state value.
            increment: Value to increment state value.
            decrement: Value to decrement state value.

        Returns:
            Tuple of values.

        See Also:
            https://reactjs.org/docs/hooks-state.html

        Todos:
            * Add better docstring for this method.
            * Add increment and decrement operations.
        """
        increment_or_decrement = self.__set_incremental_or_decremental(
            increment=increment, decrement=decrement, default_value=self.values[name]
        )
        if self.is_functional:
            return self._set_functional_state(
                name, self.values[name], incr_or_decr_val=increment_or_decrement
            )
        return self._set_class_state(name, incr_or_decr_val=increment_or_decrement)

    def use_effect(
        self, name: str, default_value: Optional[Any] = None
    ) -> tuple[str, str]:
        """Wrapper around React useEffect hook.

        Args:
            name: Name of state value.
            default_value: Default of state value.

        Returns:
            Tuple of values.

        See Also:
            https://reactjs.org/docs/hooks-effect.html

        Todos:
            * Add better docstring for this method + complete logic.
        """
        raise NotImplementedError

    def _set_class_state(
        self, name: str, incr_or_decr_val: str
    ) -> tuple[Function, str]:
        """Sets state in class format.

        Args:
            incr_or_decr_val: Increment or decrement by specific value, if either enabled.
            name: Name of state value.
        """
        state_output = f"set{name.title()}"
        set_state_dict = js_utils.add_curls(f"{name} : {name}New {incr_or_decr_val}")
        state_function = js_utils.add_this(f"setState({set_state_dict});")
        class_state = js_utils.add_class_state(name)
        function = Function(
            value=class_state,
            name=state_output,
            is_functional=self.is_functional,
        )
        self.functions.append(f"{state_output} = ({name}New) => {state_function}")
        var = function, js_utils.add_curls(class_state)
        return var

    def _set_functional_state(
        self, name: str, default_value: Any, incr_or_decr_val: str
    ) -> tuple[Function, str]:
        """Sets state in functional format.

        Args:
            incr_or_decr_val: Increment or decrement by specific value, if either enabled.
            name: Name of state value.
            default_value: default for passed state key.
        """
        function_name = f"set{name.title()}"
        state_output = f"const [{name}, {function_name}]"
        state_function = f"React.useState({json.dumps(default_value)});"
        function_repr = f"{state_output} = {state_function}"
        function = Function(
            value=f"{name} {incr_or_decr_val}",
            name=function_name,
            is_functional=self.is_functional,
        )
        self.functions.append(function_repr)
        var = function, js_utils.add_curls(name)
        return var

    @staticmethod
    def __set_incremental_or_decremental(
        increment: Optional[Union[int, str]],
        decrement: Optional[Union[int, str]],
        default_value: Union[int, str],
    ) -> str:
        if increment or decrement:
            if increment and decrement:
                raise KeyError(
                    "incremental and decremental values may not be passed together."
                )
            elif not str(default_value).isnumeric():
                raise KeyError(
                    "default_value must be a numeric when using incremental or decremental arguments."
                )
            elif (increment or decrement) < 1:
                raise ValueError("incremental and decremental values must be positive.")
            return f" + {increment}" if increment else f" - {decrement}"
        return ""

    def __getitem__(self, item: Any) -> Any:
        return self.values[item]


class Props(_ProtocolProps):
    """Public class representation of React props.

    Expected value is a state object.

    Examples:
        `props = Props(state)`
    """

    is_functional = (
        False  #: Determines whether prop object is contained in a functional component.
    )

    def __init__(self, state: Optional[State] = None) -> None:
        self.state = state
        self.values = state.values if state else {}
        self.type = self.__class__.__name__.lower()

    def as_json(self) -> str:
        """Return dict as json."""
        return json.dumps(self.values)

    def __getitem__(self, item: Any) -> str:
        if self.state.is_functional:
            return js_utils.add_curls(js_utils.add_props(item))
        return js_utils.add_curls(js_utils.add_class_props(item))
