from setuptools import setup, find_packages

setup(
    name="JapaneseMatplotlib",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
    ],
    author="kiendt",
    author_email="kiendt226@gmail.com",
    description="A package to support Japanese fonts for Matplotlib",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='MIT License',
    include_package_data=True,
    package_data={
        'JapaneseMatplotlib': ['fonts/*'],
    }
)
