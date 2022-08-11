"""Core functionality of React Native class based components."""
import json
from functools import singledispatchmethod
from typing import Optional, Union

from sweetpotato.config import settings
from sweetpotato.core import ThreadSafe
from sweetpotato.core.base_management import BaseProps, BaseState
from sweetpotato.core.protocols import (
    ComponentVar,
    CompositeVar,
    CompositeType,
    ComponentType,
)


class Component:
    """Base React Native component with MetaComponent metaclass.

    Args:
        children: Inner content for component.
        variables: Contains variables (if any) belonging to given component.
        kwargs: Arbitrary keyword arguments.

    Attributes:
        _children: Inner content for component.
        _attrs: String of given attributes for component.
        _variables: Contains variables (if any) belonging to given component.
        props: Allowed props for component.
        parent: Name of parent component, defaults to `'App'`.

    Example:
        component = Component(children="foo")
    """

    package: str = "react-native"  #: Default package for component.
    props: set = {
        "state",
        "props",
    }  #: Set of allowed props for component, default `'state'`, `'props'`.
    is_composite: bool = False  #: Indicates whether component may have inner content.

    def __init__(
        self,
        component_name: Optional[str] = None,
        children: Optional[str] = None,
        state: Optional[BaseState] = BaseState(),
        props: Optional[BaseProps] = BaseProps(),
        variables: Optional[list[str]] = None,
        **kwargs,
    ) -> None:
        self.component_name = (
            component_name if component_name else self._set_default_name()
        )
        if set(kwargs.keys()).difference(self.props):
            attributes = ", ".join(set(kwargs.keys()).difference(self.props))
            raise AttributeError(
                f"{self.component_name} component does not have attribute(s): {attributes}"
            )
        self._import_name = (
            component_name if component_name else self._set_default_name()
        )

        self._children = children
        self._state = state
        self._props = props
        self._variables = variables if variables else []
        self.parent = settings.APP_COMPONENT
        self._attrs = kwargs

    @property
    def import_name(self) -> Optional[str]:
        """Name of component import."""
        return self._import_name

    @import_name.setter
    def import_name(self, name) -> None:
        self._import_name = name

    @property
    def children(self) -> Optional[str]:
        """Property returning inner content."""
        return self._children

    @property
    def variables(self) -> Optional[str]:
        """Property returning string of variables (if any) belonging to given component."""
        return "\n".join(self._variables)

    @property
    def attrs(self) -> Optional[str]:
        """Property string of given attributes for component"""
        return " ".join([self._format_attr(v, k) for k, v in self._attrs.items()])

    def _make_attrs(self, attr: Union[BaseState, BaseProps]) -> str:
        placeholder = "" if self.is_composite else "this."
        attr_type = f"{placeholder}{attr.type}"
        return " ".join(
            [f"{k}={'{'}{attr_type}.{k}{'}'}" for k, v in attr.values.items()]
        )

    @singledispatchmethod
    def _format_attr(self, attr, key) -> None:
        """Generic method for formatting state, props & style.

        Args:
            key: ...
            attr: ...
        """
        raise AttributeError(f"{attr} {key} not in allowed types")

    @_format_attr.register(BaseState)
    @_format_attr.register(BaseProps)
    def _(self, attr: Union[BaseState, BaseProps], _) -> str:
        return self._make_attrs(attr)

    @_format_attr.register(str)
    def _(self, attr: dict, key: str) -> str:
        return f"{key}={'{'}{attr}{'}'}"

    @_format_attr.register
    def _(self, attr: bool, key: str) -> str:
        return f"{key}={'{'}{json.dumps(attr)}{'}'}"

    def _set_default_name(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        if self._children:
            return f"<{self.component_name} {self.attrs}>{self.children}</{self.component_name}>"
        return f"<{self.component_name} {self.attrs}/>"


class Composite(Component):
    """Base React Native component with MetaComponent metaclass.

    Args:
        children: Inner content for component.
        state: Dictionary of allowed state values for component.
        functions: Functions for component, passed to top level component.
        kwargs: Arbitrary keyword arguments.

    Attributes:
        _children: Inner content for component.
        _state: Dictionary of allowed state values for component.
        _functions: Functions for component, passed to top level component.

    Example:
        composite = Composite(children=[])
    """

    is_context: bool = False  #: Indicates whether component is a context, similar to an inline if-else.
    is_composite: bool = True  #: Indicates whether component may have inner components.
    is_root: bool = False  #: Indicates whether component is a top level component.

    def __init__(
        self,
        children: Optional[list[Union[ComponentVar, CompositeVar]]] = None,
        functions: Optional[list[str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._children = children if children else []
        self._functions = functions if functions else []

    @property
    def children(self) -> str:
        """Property returning a string rendition of child components"""
        return "".join(map(repr, self._children))

    @property
    def functions(self) -> Optional[str]:
        """Property returning string of variables (if any) belonging to given component."""
        return "".join(self._functions)

    def __repr__(self) -> str:
        if self._children and self.is_composite:
            return f"<{self.component_name} {self.attrs}>{self.children}</{self.component_name}>"
        return f"<{self.component_name} {self.attrs}/>"


class ComponentRegistry(metaclass=ThreadSafe):
    """Registry of components in React Native tree.

    Todos:
        * Complete docstrings for class + methods.
    """

    _registry = {}

    @classmethod
    @property
    def registry(cls):
        """

        Returns:

        """
        return cls._registry

    @classmethod
    def register(cls, component):
        """

        Args:
            component:
        """
        if component.component_name not in cls._registry.keys():
            cls._registry[component.component_name] = component


class RootComponent(Composite):
    """Root component.

    Args:
        component_name: Name of .js class/function/const for component.
        kwargs: Arbitrary keyword arguments.

    Attributes:
        component_name: Name of .js class/function/const for component.
        import_name: Name of .js class/function/const for component import.
    """

    is_composite = False  #: Indicates whether component is represented as composite inside parent component.
    package_root: str = f"./{settings.SOURCE_FOLDER}/components"
    is_root: bool = True  #: Indicates whether component is a top level component.
    is_functional: bool = (
        False  #: Indicates whether component a functional or class component.
    )

    def __init__(
        self,
        extra_imports: Optional[dict[str, Union[str, set]]] = None,
        **kwargs,
    ) -> None:
        if len(kwargs.get("component_name", "").split(" ")) > 1:
            kwargs["component_name"] = "".join(
                [word.title() for word in kwargs.get("component_name").split(" ")]
            )
        super().__init__(**kwargs)
        if self._state.functions:
            self._functions.extend(self._state.functions)
        self.package = f"{self.package_root}/{self._import_name}.js"
        self._imports = {}
        self._set_parent(self._children)
        if extra_imports:
            self._imports.update(extra_imports)
        ComponentRegistry.register(self)

    @property
    def imports(self) -> Optional[str]:
        """Property returning string of imports (if any) belonging to given component."""
        import_string = ""
        for key, value in self._imports.items():
            if value and "RootNavigation" != list(value)[0]:
                import_string += (
                    f'import {value} from "{key}";\n'.replace("'", "")
                    if value
                    else f'import "{key}"\n'
                )

        return import_string

    @property
    def state(self) -> Optional[str]:
        """Property returning json string of state (if any) belonging to given component."""
        return self._state.as_json()

    def _set_parent(self, children: list[Union[CompositeType, ComponentType]]) -> None:
        """Sets top level component as root and sets each parent to self.

        Args:
            children: List of components.
        """
        for child in children:
            child.parent = self.component_name
            if (child.is_composite and not child.is_context) or not child.is_composite:
                if child.package not in self._imports:
                    self._imports[child.package] = set()
                self._imports[child.package].add(child.import_name)
            if child.is_composite:
                self._functions.append(child.functions)
                self._variables.append(child.variables)
                self._set_parent(child._children)

    def serialize(self, as_format: Optional[str] = "dict") -> dict:
        """Returns component as specified serialization format.

        Args:
            as_format: Specified format, one of `'json', `'dict'``, `'dict'` is default.

        Returns:
            Serialized component.

        Todos:
            * Add formatting logic for json.
        """

        if as_format == "json":
            raise NotImplementedError
        return {
            "state": self.state,
            "variables": self.variables,
            "functions": self.functions,
            "children": self.children,
            "imports": self.imports,
            "package": self.package,
            "functional": self.is_functional,
            "props": self.props,
        }

    @classmethod
    def register(cls, obj: Union[BaseState, BaseProps]) -> None:
        """Registers state/prop object as functional or class based.

        Args:
            obj: State or Prop object.
        """
        obj.is_functional = cls.is_functional


class App(RootComponent):
    """Expo entry class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.package = f"{settings.REACT_NATIVE_PATH}/{self.import_name}.js"
