from setuptools import setup, find_packages

setup(
    name="bm_api_dev",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],
    author="Kan-Jen Liu",
    author_email="kanjen.liu@sixense-group.com",
    description="This is a test helper package for Beyond Monitoring API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sixense-Data-Manager/bm-api-dev",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
