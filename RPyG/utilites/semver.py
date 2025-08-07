from typing import Any


class SemVerException(Exception):
    """Exception raised for invalid semantic version strings."""

    def __init__(self, input_string: str):
        self.input_string = input_string
        Exception.__init__(
            self,
            f"'{input_string}' can't be converted to SemVerString. "
            f"Must be in format X.Y.Z (e.g., '1.0.0') and not start with 'v'",
        )


class SemVerString:
    version: str
    values: tuple[int, int, int]

    def __init__(self, input_string: str):
        version_digits = input_string.split(".")
        if version_digits[0].startswith("v"):
            raise SemVerException(input_string)
        match len(version_digits):
            case 3:
                try:
                    major_version = int(version_digits[0])
                    minor_version = int(version_digits[1])
                    patch_version = int(version_digits[2])
                except ValueError:
                    raise SemVerException(input_string)
                self.version = f"{major_version}.{minor_version}.{patch_version}"
                self.values = (major_version, minor_version, patch_version)
            case _:
                raise SemVerException(input_string)

    def __str__(self):
        return self.version

    def __repr__(self):
        return f"SemVerString('{self.version}')"

    def __eq__(self, value: Any):
        match isinstance(value, SemVerString):
            case False:
                return NotImplemented
            case True:
                value: SemVerString
                return self.values == value.values
            case _:
                raise RuntimeError(
                    "isinstance() returned non boolean value, inform pannenkoek of the bitflip"
                )

    def __lt__(self, value: Any):
        match isinstance(value, SemVerString):
            case False:
                return NotImplemented
            case True:
                value: SemVerString
                return self.values < value.values
            case _:
                raise RuntimeError(
                    "isinstance() returned non boolean value, inform pannenkoek of the bitflip"
                )

    def __gt__(self, value: Any):
        match isinstance(value, SemVerString):
            case False:
                return NotImplemented
            case True:
                value: SemVerString
                return self.values > value.values
            case _:
                raise RuntimeError(
                    "isinstance() returned non boolean value, inform pannenkoek of the bitflip"
                )

    def __le__(self, value: Any):
        match isinstance(value, SemVerString):
            case False:
                return NotImplemented
            case True:
                value: SemVerString
                return self.values <= value.values
            case _:
                raise RuntimeError(
                    "isinstance() returned non boolean value, inform pannenkoek of the bitflip"
                )

    def __ge__(self, value: Any):
        match isinstance(value, SemVerString):
            case False:
                return NotImplemented
            case True:
                value: SemVerString
                return self.values >= value.values
            case _:
                raise RuntimeError(
                    "isinstance() returned non boolean value, inform pannenkoek of the cosmic bitflip"
                )

    def __hash__(self):
        return hash(self.values)
