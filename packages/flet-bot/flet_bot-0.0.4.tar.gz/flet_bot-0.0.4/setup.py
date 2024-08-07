from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.4'
DESCRIPTION = 'Simplify the development of a Telegram bot'
LONG_DESCRIPTION = 'A package that allows you to create telegram bots faster, more flexible and easier'

# Setting up
setup(
    name="flet_bot",
    version=VERSION,
    author="Rarenats (Dmitriy Rarenastu)",
    author_email="<>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyTelegramBotAPI', 'APScheduler', 'asyncio', 'aiohttp',' loguru'],
    keywords=['python', 'telegram bot', 'telegram bots', 'telegram', 'bot', 'bots'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)