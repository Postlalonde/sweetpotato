"""Contains classes based on UI Kitten components.

See `UI Kitten <https://akveo.github.io/react-native-ui-kitten/docs/components/components-overview>`_
"""
from typing import Optional

from sweetpotato.core.base import Component, Composite
from sweetpotato.props.ui_kitten_props import (
    ICON_REGISTRY_PROPS,
    APPLICATION_PROVIDER_PROPS,
    LAYOUT_PROPS,
    BUTTON_PROPS,
    TEXT_PROPS,
    INPUT_PROPS,
)


class IconRegistry(Component):
    """Implementation of ui-kitten IconRegistry component.

    See `<https://akveo.github.io/react-native-ui-kitten/docs/components/icon/overview#icon>`_
    """

    package: str = "@ui-kitten/components"  #: Default package for component.
    props: set = ICON_REGISTRY_PROPS  #: Set of allowed props for component.


class ApplicationProvider(Composite):
    """Implementation of ui-kitten ApplicationProvider component.

    See https://akveo.github.io/react-native-ui-kitten/docs/components/application-provider

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    package: str = "@ui-kitten/components"  #: Default package for component.
    props: set = APPLICATION_PROVIDER_PROPS  #: Set of allowed props for component.

    def __init__(self, **kwargs) -> None:
        kwargs.update(
            {
                "children": [
                    IconRegistry(icons="EvaIconsPack"),
                    kwargs.pop("children")[0],
                ]
            }
        )
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<{self._import_name} {'{'}...eva{'}'}{self.attrs}>{self.children}</{self._import_name}>"


class Text(Component):
    """Implementation of ui-kitten Text component.

    See https://akveo.github.io/react-native-ui-kitten/docs/components/text.
    """

    package: str = "@ui-kitten/components"  #: Default package for component.
    props: set = TEXT_PROPS  #: Set of allowed props for component.

    def __init__(self, text: Optional[str] = None, **kwargs) -> None:
        super().__init__(children=text, **kwargs)


class Button(Composite):
    """Implementation of ui-kitten Button component.

    See https://akveo.github.io/react-native-ui-kitten/docs/components/button.
    """

    package: str = "@ui-kitten/components"  #: Default package for component.
    props: set = BUTTON_PROPS  #: Set of allowed props for component.

    def __init__(self, **kwargs) -> None:
        super().__init__(children=[Text(text=kwargs.pop("title"))], **kwargs)


class Input(Component):
    """Implementation of ui-kitten Input component.

    See https://akveo.github.io/react-native-ui-kitten/docs/components/input.
    """

    package: str = "@ui-kitten/components"  #: Default package for component.
    props: set = INPUT_PROPS  #: Set of allowed props for component.


class Layout(Composite):
    """Implementation of ui-kitten Layout component.

    See https://akveo.github.io/react-native-ui-kitten/docs/components/layout.
    """

    package: str = "@ui-kitten/components"  #: Default package for component.
    props: set = LAYOUT_PROPS  #: Set of allowed props for component.
