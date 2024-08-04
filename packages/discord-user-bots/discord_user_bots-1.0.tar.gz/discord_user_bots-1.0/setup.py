from setuptools import setup, find_packages

setup(
    name='discord-user-bots',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "pydantic", "requests", "aiohttp", "cachetools",
        "pyclean"
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ваше Имя',
    url='https://github.com/CCCProo/discord_user_bot',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        '': ['type/*', 'error/*'],
    },
)
