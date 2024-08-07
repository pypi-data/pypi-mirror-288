def add_driver_to_url(url: str) -> str:
    return f"postgresql+asyncpg://{url}"
