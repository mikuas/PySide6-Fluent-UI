from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PySide6-Fluent-UI',
    version='0.0.5',
    author='Mikuas',
    packages=find_packages(),
    description="A fluent design widgets library based on PySide6",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPLv3",
    install_requires=[
        "PySide6>=6.8.1.1",
        "PySide6-Fluent-Widgets[full]>=1.8.7",
        "PySideSix-Frameless-Window>=0.7.3",
        "pynput>=1.8.1"
    ]
)