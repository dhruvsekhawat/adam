from setuptools import setup, find_packages

setup(
    name="adam-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi[all]",
        "sqlalchemy",
        "alembic",
        "psycopg2-binary",
        "python-dotenv",
    ],
) 