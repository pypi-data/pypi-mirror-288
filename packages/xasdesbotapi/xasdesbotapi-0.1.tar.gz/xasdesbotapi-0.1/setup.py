from setuptools import setup, find_packages

setup(
    name='xasdesbotapi',
    version='0.1',
    description='Managing Xasdes Bot commands',
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
