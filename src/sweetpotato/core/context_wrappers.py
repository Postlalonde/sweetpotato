"""
Todo:
    * Add docstrings for all classes & methods.
    * Add typing.
"""
from abc import abstractmethod, ABC
from typing import Union, Optional

from sweetpotato.authentication import AuthenticationProvider
from sweetpotato.components import SafeAreaProvider
from sweetpotato.config import settings
from sweetpotato.core import js_utils
from sweetpotato.core.base import App
from sweetpotato.core.base_management import State
from sweetpotato.core.protocols import CompositeType
from sweetpotato.navigation import NavigationContainer
from sweetpotato.ui_kitten import ApplicationProvider


class Wrapper(ABC):
    """Wrapping interface for components."""

    @abstractmethod
    def wrap(self, component, **kwargs) -> CompositeType:
        """Abstract component wrapping."""
        return component


class UIKittenWrapper(Wrapper):
    """Adds UI Kitten support to app."""

    def wrap(self, component: CompositeType, **kwargs) -> CompositeType:
        """Wraps component in UI Kitten if enabled.

        Args:
            component: ...

        Returns:
            Composite.
        """
        if settings.USE_UI_KITTEN:
            theme = kwargs.pop("theme", None)
            if not theme:
                raise KeyError("UI Kitten must be provided a theme.")
            component = ApplicationProvider(
                children=[component], theme=js_utils.add_curls(f"...eva.{theme}")
            )
        return super().wrap(component, **kwargs)


class AuthenticationWrapper(Wrapper):
    """Adds authentication plugins to app.

    Todo:
        * Add docstrings.
    """

    def wrap(self, component: CompositeType, **kwargs) -> CompositeType:
        """Wraps component in AuthenticationProvider if enabled.

        Args:
            component (Composite): ...

        Returns:
            Composite.
        """
        if settings.USE_AUTHENTICATION:
            component = AuthenticationProvider(children=[component])
        return super().wrap(component, **kwargs)


class NavigationWrapper(Wrapper):
    """Adds NavigationContainer component to app and gives navigation capability.

    Todo:
        * Add docstrings.
    """

    def wrap(self, component: CompositeType, **kwargs) -> CompositeType:
        """Wraps component in NavigationContainer if enabled.

        Args:
            component (Composite): ...

        Returns:
            Composite.
        """
        if settings.USE_NAVIGATION:
            component = NavigationContainer(
                children=[component], ref="RootNavigation.navigationRef"
            )
        return super().wrap(component, **kwargs)


class SafeAreaWrapper(Wrapper):
    """Adds react-native-safe-area-context SafeAreaProvider component to app.


    Todo:
        * Add docstrings
    """

    def wrap(self, component: CompositeType, **kwargs) -> CompositeType:
        """Wraps component in SafeAreaProvider.

        Args:
            component (Composite): ...

        Returns:
            Composite.
        """
        component = SafeAreaProvider(children=[component])
        return super().wrap(component, **kwargs)


class ContextWrapper(
    AuthenticationWrapper, SafeAreaWrapper, UIKittenWrapper, NavigationWrapper
):
    """Checks for and adds navigation, authentication, and ui-kitten contexts.

    Todo:
        * Add docstrings
    """

    def wrap(
        self,
        component: Union[CompositeType, None],
        state: Optional[State] = None,
        is_functional: Optional[bool] = False,
        **kwargs,
    ) -> "App":
        """Checks and wraps component in provided wrappers, if configured.

        Args:
            is_functional:
            state:
            component (Composite): ...

        Returns:
            Composite.
        """
        if not state:
            state = State(
                {
                    "authenticated": False,
                }
            )

        component = App(children=[super().wrap(component, **kwargs)], state=state)
        extra_imports = {}
        if settings.USE_NAVIGATION:
            extra_imports.update(
                {
                    "react-native-gesture-handler": None,
                    "./src/components/RootNavigation": "* as RootNavigation",
                }
            )
        if settings.USE_UI_KITTEN:
            extra_imports.update(
                {
                    "@eva-design/eva": "* as eva",
                    "@ui-kitten/eva-icons": {"EvaIconsPack"},
                }
            )
        return component
