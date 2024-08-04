from setuptools import setup, find_packages

setup(
    name="stone_in_waiting",
    version="0.0.1",
    author="Shuai Zeng",
    author_email="maillinger@gmail.com",
    description="Please refer to the paper for details.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/beastsenior/stone_in_waiting.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
    license="MIT",
)
