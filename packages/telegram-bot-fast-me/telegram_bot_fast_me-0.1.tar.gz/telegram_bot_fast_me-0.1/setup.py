from setuptools import setup, find_packages

setup(
    name="telegram-bot-fast-me",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'aiohttp',
    ],
    author="Your Name",
    author_email="parker.trusty@echohyper.com",
    description="A fast and simple library for Telegram bots",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/TelegramBotFastMe",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)