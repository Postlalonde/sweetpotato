"""Contains classes based on React Navigation components.


See `React Navigation <https://reactnavigation.org/docs/getting-started/#>`_
"""

from typing import Optional

from sweetpotato.config import settings
from sweetpotato.core import js_utils
from sweetpotato.core.base import Composite, RootComponent
from sweetpotato.core.protocols import CompositeVar
from sweetpotato.management import State
from sweetpotato.props.navigation_props import (
    NAVIGATION_CONTAINER_PROPS,
    ROOT_NAVIGATION_PROPS,
    SCREEN_PROPS,
    BASE_NAVIGATOR_PROPS,
    NATIVE_STACK_NAVIGATOR_PROPS,
    BOTTOM_TAB_NAVIGATOR_PROPS,
)


class RootNavigation(RootComponent):
    """React Navigation component based on navigating without the prop.

    Based on https://reactnavigation.org/docs/navigating-without-navigation-prop/
    so that we don't have to pass the prop between screens.
    """

    is_functional: bool = (
        True  #: Indicates whether component a functional or class component.
    )
    is_composite: bool = False  #: Indicates whether component may have inner content.
    is_context: bool = (
        True  #: Indicates whether component is a context, similar to an inline if-else.
    )
    props: set = ROOT_NAVIGATION_PROPS  #: Set of allowed props for component.

    def __init__(self, **kwargs):
        super().__init__(
            functions=settings.NAVIGATION_FUNCTIONS,
            extra_imports={
                "@react-navigation/native": {
                    "CommonActions",
                    "createNavigationContainerRef",
                    "DrawerActions",
                    "StackActions",
                },
            },
            **kwargs,
        )

    def __repr__(self):
        return ""


class NavigationContainer(Composite):
    """React Navigation NavigationContainer component."""

    package: str = "@react-navigation/native"  #: Default package for component.
    props: set = NAVIGATION_CONTAINER_PROPS  #: Set of allowed props for component.


class Screen(RootComponent):
    """React Navigation Screen component.

    Args:
        screen_type: Navigator name/type prefix, shown as {screen_name}.Screen.
        screen_name: Name of screen.
        kwargs: Arbitrary keyword arguments.

    Attributes:
        screen_type: Navigator name/type prefix, shown as {screen_name}.Screen.
    """

    package_root: str = (
        f"./{settings.SOURCE_FOLDER}/screens"  #: Default package for component.
    )
    props: set = SCREEN_PROPS  #: Set of allowed props for component.
    is_composite = False  #: Indicates whether component may have inner content.

    def __init__(
        self,
        screen_type: str,
        screen_name: str,
        is_functional: bool,
        **kwargs,
    ) -> None:
        self.is_functional = is_functional
        super().__init__(component_name=screen_name, **kwargs)
        self.screen_type = f"{screen_type}.{self._set_default_name()}"
        self.component_name = self.screen_type

        self.is_functional = is_functional

    def __repr__(self) -> str:
        children = f"{'{'}'{self.import_name}'{'}'}>{'{'}() => <{self.import_name} {self.attrs}/> {'}'}"
        return f"<{self.component_name} name={children}</{self.component_name}>"


class BaseNavigator(Composite):
    """Abstraction of React Navigation Base Navigation component.

    Args:
        name: Name/type of navigator.
        kwargs: Arbitrary keyword arguments.

    Attributes:
        name: Name/type of navigator.

    Todo:
        * Add specific props from React Navigation.
    """

    props: set = BASE_NAVIGATOR_PROPS  #: Set of allowed props for component.

    def __init__(self, name: str = None, **kwargs) -> None:
        super().__init__(component_name=self._set_custom_name(name), **kwargs)
        self._variables = [
            js_utils.make_const(self.component_name, f"{self.import_name}()")
        ]
        self.component_name = f"{self.component_name}.Navigator"
        self._children.append(RootNavigation())

    @staticmethod
    def _set_custom_name(name: Optional[str]) -> str:
        if name:
            component_name = name.split(".")
            component_name[0] = name
            return (".".join(component_name)).title()
        return name

    def screen(
        self,
        screen_name: str,
        children: CompositeVar,
        functions: Optional[list] = None,
        state: Optional[State] = None,
        is_functional: bool = False,
        extra_imports: Optional[dict[str, str]] = None,
    ) -> None:
        """Instantiates and adds screen to navigation component and increments screen count.

        Args:
            is_functional: Boolean indicating whether screen is a functional component, default false.
            extra_imports: Any additional imports required by the screen file.
            screen_name: Name of screen component.
            children: List of child components.
            functions: String representation of .js functions for component.
            state: Dictionary of applicable state values for component.
        """
        screen_type = self.component_name.split(".")[0]
        self._children.append(
            Screen(
                screen_name=screen_name,
                screen_type=screen_type,
                children=children,
                functions=functions,
                state=state,
                is_functional=is_functional,
                extra_imports=extra_imports,
            )
        )


class Stack(BaseNavigator):
    """Abstraction of React Navigation StackNavigator component.

    See https://reactnavigation.org/docs/stack-navigator
    """

    import_name: str = "createNativeStackNavigator"  #: Name of component import.
    package: str = "@react-navigation/native-stack"  #: Default package for component.
    props: set = NATIVE_STACK_NAVIGATOR_PROPS  #: Set of allowed props for component.


class Tab(BaseNavigator):
    """Abstraction of React Navigation TabNavigator component.

    See https://reactnavigation.org/docs/bottom-tab-navigator
    """

    import_name: str = "createBottomTabNavigator"  #: Name of component import.
    package: str = "@react-navigation/bottom-tabs"  #: Default package for component.
    props: set = BOTTOM_TAB_NAVIGATOR_PROPS  #: Set of allowed props for component.


def create_bottom_tab_navigator(name: Optional[str] = None) -> Tab:
    """Function representing the createBottomTabNavigator function in react-navigation.

    Args:
        name: name of navigator, this is necessary if there are multiple navigators in the same app.

    Returns:
        Tab navigator object with specified name, if passed.
    """
    return Tab(name=name)


def create_native_stack_navigator(name: Optional[str] = None) -> Stack:
    """Function representing the createNativeStackNavigator function in react-navigation.

    Args:
        name: name of navigator, this is necessary if there are multiple navigators in the same app.

    Returns:
        Stack navigator object with specified name, if passed.
    """
    return Stack(name=name)
