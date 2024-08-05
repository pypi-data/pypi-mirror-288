from setuptools import setup, find_packages

setup(
    name="github_module",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Pavan Bhatt",
    author_email="pavanhbhatt1@gmail.com",
    description="Modules for interacting with GitHub API.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="",
)
