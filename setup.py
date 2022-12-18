import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="argofamiglia",
    version="0.1.2",
    author="Salvatore Abello",
    author_email="salvatore.abello2005@gmail.com",
    description="An API wrapper created to interface Python with Argo ScuolaNext.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salvatore-abello/argofamiglia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests'
    ],
    keywords='argofamiglia argo argoscuolanext python scuolanext ',
    project_urls={
        'Homepage': 'https://github.com/salvatore-abello/argofamiglia',
    }
)
