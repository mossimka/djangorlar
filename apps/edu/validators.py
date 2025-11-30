
def indentation_validator(indentation: int) -> None:
    if indentation > 5 or indentation < 0:
        raise ValueError("Indentation must be 0 to 5 inclusive.")