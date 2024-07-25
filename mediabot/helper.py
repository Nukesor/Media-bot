import validators


def url_from_text(text: str) -> str | None:
    """Try to find a line inside of some multi-line text that contains a valid link."""
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if validators.url(line):
            return line

        continue

    # We didn't find a line that contains a valid link
    return None
