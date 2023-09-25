from typing import Protocol


def star_fill(size: int) -> str:
    return "*" * size


class RandomTextGenerator(Protocol):
    def __call__(self, size: int) -> str:
        ...


def obfuscate_text(
    s: str,
    starting_chars_to_keep: int = 2,
    ending_chars_to_keep: int = 2,
    generate_obfuscated_text: RandomTextGenerator = star_fill,
) -> str:
    non_obfuscated_chars = starting_chars_to_keep + ending_chars_to_keep
    remaining_chars = len(s) - non_obfuscated_chars
    if remaining_chars <= 0:
        return generate_obfuscated_text(size=len(s))
    return "{prefix}{obfuscated}{suffix}".format(
        prefix=s[:starting_chars_to_keep],
        obfuscated=generate_obfuscated_text(size=remaining_chars),
        suffix=s[-ending_chars_to_keep:],
    )
