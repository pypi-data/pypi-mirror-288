from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as description:
    long_description: str = description.read()

setup(
    name="air-migrations",
    python_requires=">=3.11.0",
    version="1.0.0",
    author="MSNLP",
    description="Portable migrations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["__pycache__"]),
    install_requires=[
        "alembic>=1.13.2,<2.0.0",
        "sqlalchemy>=2.0.31,<3.0.0",
        "asyncpg>=0.29.0,<1.0.0",
        "greenlet>=3.0.3,<4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "migrate=air_migrations.cli:main",
        ],
    },
)
