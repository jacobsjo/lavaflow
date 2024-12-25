from typing import TypedDict

VerticalAnchor = TypedDict('Absolute', {'absolute': int}) | TypedDict('AboveBottom', {'above_bottom': int}) | TypedDict('BelowTop', {'below_top': int})

def absolute(value: int) -> VerticalAnchor:
    return dict(
        absolute=value
    )

def above_bottom(value: int) -> VerticalAnchor:
    return dict(
        above_bottom=value
    )

def below_top(value: int) -> VerticalAnchor:
    return dict(
        below_top=value
    )
