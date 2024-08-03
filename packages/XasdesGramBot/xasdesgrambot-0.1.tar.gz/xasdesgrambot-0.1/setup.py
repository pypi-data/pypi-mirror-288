from setuptools import setup, find_packages

setup(
    name='XasdesGramBot',
    version='0.1',
    description='Эта библиотека созданная разработчиком Xasdes для создания телеграм ботов',
    author='Xasdes',
    author_email='xasdestest@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    tests_require=[
        'unittest',
    ],
    python_requires='>=3.6',
)
