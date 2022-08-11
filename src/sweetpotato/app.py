"""Provider for React Native entry.

Todos:
    * Add module docstrings
"""
from typing import Optional

from sweetpotato.components import View
from sweetpotato.core.base_management import BaseState
from sweetpotato.core.build import Build
from sweetpotato.core.context_wrappers import ContextWrapper
from sweetpotato.core.protocols import CompositeVar


def default_screen() -> CompositeVar:
    """Default welcome screen for application.

    Returns:
        Welcome screen for application.

    Todo:
        * Add actual welcome screen.
    """
    return View()


class App:
    """Provides methods for interacting with underlying :class:`sweetpotato.core.build.Build` class.

    Args:
        component: Top level component, default is the sweetpotato welcome screen.
        context: Context wrapper for application.
        build: Build tools for application.
        theme: Theme of @eva-design/eva, one of dark, light.
        kwargs: Arbitrary keyword arguments.

    Examples:
        `app = App()`
    """

    def __init__(
        self,
        component: Optional[CompositeVar] = None,
        context: Optional[ContextWrapper] = ContextWrapper(),
        build: Optional[Build] = Build(),
        theme: Optional[str] = None,
        state: Optional[BaseState] = None,
        **kwargs
    ) -> None:
        self._context = context
        self._build = build
        self._context.wrap(
            component if component else default_screen(),
            theme=theme,
            state=state,
            **kwargs
        )

    def run(self, platform: Optional[str] = None) -> None:
        """Starts a React Native expo client through a subprocess.

        Args:
            platform: Platform for expo to run application on, one of ios, android, and web.
        """
        self._build.run(platform=platform)

    def publish(self, platform: str) -> None:
        """Publishes app to specified platform / application store.

        Args:
            platform: Platform for app to be published on.
        """
        self._build.publish(platform=platform)

    def write_files(self) -> None:
        """Writes js files without running the application."""
        self._build.write_files()

    def show(self) -> str:
        """Returns string .js rendition of application.

        Returns:
            String rendition of application in .js format.
        """
        return self._build.show()
