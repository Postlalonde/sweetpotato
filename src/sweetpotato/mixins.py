"""Provides mixin classes for component customization.

Examples:

    from sweetpotato.core.base import RootComponent
    from sweetpotato.mixins import CustomMixin

    class CustomComponent(RootComponent, CustomMixin):
        extra_props = {"custom_prop"}

Todos:
    * Implement mixins for custom component.
"""


class CustomMixin:
    """Mixin customization methods, meant to be subclassed with RootComponent class.

    Examples:

        from sweetpotato.core.base import RootComponent
        from sweetpotato.mixins import CustomMixin

        class CustomComponent(RootComponent, CustomMixin):
            extra_props = {"custom_prop"}
    """

    extra_props: set = set()  #: Set of extra allowed props for component, set by user.

    def __init__(self) -> None:
        if self.extra_props:
            # noinspection PyUnresolvedReferences
            self.props.update(self.extra_props)
