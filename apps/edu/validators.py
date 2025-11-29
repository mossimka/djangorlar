
def indentation_validator(indentation: int) -> None:
    if not indentation.isdigit() or indentation > 5 or indentation < 0:
        raise ValueError("Indentation must be 0 to 5 inclusive.")