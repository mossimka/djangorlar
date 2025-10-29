"""
Configuration file holding constants for the
application. Contains metadata, defaults, and
placeholder values.
"""



APP_NAME: str = "MyPythonApp"
VERSION: str = "0.1.0"
AUTHOR: str = "Student"
LICENSE = "MIT"


SETTINGS: dict[str, bool | int | str] = {
    "debug": True,
    "max_items": 30,
    "theme": "light",
}


# Additional filler configuration placeholders
OPTIONS: list[str] = [f"option_{i}" for i in range(20)]
DEFAULT_TIMEOUTS: dict[str, int] = {
    "connect": 5,
    "read": 10,
    "write": 15,
}


# Add more sample config entries
FEATURE_FLAGS: dict[bool] = {
    "enable_logging": True,
    "use_cache": False,
    "beta_mode": True,
}


BRUH: tuple[str]  = (
    'SOMETHING',
    'SOMNETH',
    'FVSDVS',
    'DVSSD',
    'SVFSVFS',
    'SFVSF',
    'SFVSDVS',
)
