
def phone_validator(phone: str) -> None:
    if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
        raise ValueError("Phone number must be 10 to 15 digits long and contain only numbers.")