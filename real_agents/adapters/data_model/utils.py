def indent_multiline_string(multiline_string: str, indent: int = 1) -> str:
    return "\n".join("\t" * indent + line for line in multiline_string.split("\n"))
