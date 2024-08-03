from setuptools import setup

setup(
    name='hedgesql',
    version='2.0.0',
    author='HedgeDev',
    author_email='hedge_dev@mail.ru',
    description='Convenient work with sqlite3 and aiosqlite',
    packages=['hedge_sql'],
    install_requires=[
        'aiosqlite',
        'sqlite3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    python_requires='>=3.6'
)
