from setuptools import setup, find_packages

setup(
    name="pyside6_virtual_keyboard",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "PySide6",
    ],
    author="Yasin Yildirim",
    author_email="yildirimyasin1204@gmail.com",
    description="A simple virtual keyboard module using PySide6",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yasin-Yildirim/PySide6VirtualKeyboard.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.9',
)
