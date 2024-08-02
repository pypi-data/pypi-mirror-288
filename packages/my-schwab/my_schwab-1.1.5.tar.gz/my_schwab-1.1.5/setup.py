from setuptools import setup, find_packages

setup(
    name="schwab",
    version="1.0.2",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        'requests',
        'redis',
        'orjson',
        'websockets',

    ],
    extras_require={
        'redis': ['redis'],
        'mysql': ['pymysql'],
        'websocket': ['websockets'],
    }
)