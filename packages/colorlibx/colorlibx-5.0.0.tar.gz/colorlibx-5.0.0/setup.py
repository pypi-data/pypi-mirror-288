from setuptools import setup, find_packages

setup(
    name="colorlibx",
    version="5.0.0",
    description="A library for adding color to terminal text with support for 50 predefined colors, 256-color palette, and custom HEX/RGB colors.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="kawa1",
    author_email="kawa1337k@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.6',
    install_requires=[
        # Укажите зависимости, если таковые имеются
    ],
    include_package_data=True,
    package_data={
        # Если есть дополнительные данные, такие как файлы данных
    },
    keywords='color terminal text ANSI colors HEX RGB',
)

