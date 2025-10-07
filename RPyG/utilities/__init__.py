from RPyG.utilities.semver import SemVerString


def ensure_type(
    instance: object,
    expected_type: type,
    variable_name: str,
) -> None:
    if isinstance(instance, expected_type) is False:
        raise ValueError(
            f"""
The '{variable_name}' parameter must be of type {expected_type.__name__}.
Received type: {type(instance).__name__}.
"""
        )


__all__ = ["ensure_type", "SemVerString"]
