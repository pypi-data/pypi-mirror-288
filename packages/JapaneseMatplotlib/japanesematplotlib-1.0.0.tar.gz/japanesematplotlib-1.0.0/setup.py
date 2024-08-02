from setuptools import setup, find_packages

setup(
    name="JapaneseMatplotlib",
    version="1.0.0",
    packages=find_packages(),
    package_data={'JapaneseMatplotlib': ['fonts/*.ttf']},
    install_requires=[
        "matplotlib",
    ],
    author="kiendt",
    author_email="kiendt226@gmail.com",
    description="A package to support Japanese fonts for Matplotlib",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
)
