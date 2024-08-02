from setuptools import setup, find_packages

VERSION = '0.2.13'
DESCRIPTION = 'Tokenizing and processing text inputs with transformer models'
LONG_DESCRIPTION = 'A package that provides functionalities for tokenizing and processing text inputs using transformer models and other NLP tools.'

# Setting up
setup(
    name="tokenize-text",  # Updated name for readability
    version=VERSION,
    author="Urdu NLTK",  # Replace with your actual name
    author_email="urdu-nltk@uts.rf.gd",  # Replace with your actual email
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "transformers",
        "textblob",
        "requests",
        "json5",  # Use `json5` instead of `json` as `json` is part of the standard library
    ],
    keywords=['tokenization', 'text-processing', 'nlp', 'transformers'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
