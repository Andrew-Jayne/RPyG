def ensure_type(instance: object, expected_type: type, variable_name: str):
    if not isinstance(instance, expected_type):
        raise ValueError(
            f"""
The '{variable_name}' parameter must be of type {expected_type.__name__}.
Received type: {type(instance).__name__}.
"""
        )
