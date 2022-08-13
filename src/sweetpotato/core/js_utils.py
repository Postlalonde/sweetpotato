"""Provides utilities for .js rendering.

Todos:
    * Cleanup + add docstrings, typing
"""
from typing import Optional


def add_curls(val: str) -> str:
    """Adds those sweet, sweet curls."""
    return f"{'{'}{val}{'}'}"


def add_state(val: Optional[str] = "") -> str:
    """Adds state (duh)."""
    return f"state.{val}"


def add_props(val: Optional[str] = "") -> str:
    """Adds props (duh)."""
    return f"props.{val}"


def add_this(val: Optional[str] = "") -> str:
    """Adds this (duh)."""
    return f"this.{val}"


def add_class_props(val: str) -> str:
    """Adds this.props."""
    return add_this(add_props(val))


def add_class_state(val: str) -> str:
    """Adds this.state."""
    return add_this(add_state(val))


def make_const(const: str, value: str) -> str:
    """Makes a const.

    Args:
        const:
        value:

    Returns:

    """
    return f"const {const} = {value};"
