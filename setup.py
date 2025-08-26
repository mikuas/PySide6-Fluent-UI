from setuptools import setup, find_packages

setup(
    name='PySide6-Fluent-UI',
    version='0.0.3',
    author='Mikuas',
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.8.1.1",
        "PySide6-Fluent-Widgets[full]>=1.8.7"
    ]
)