from setuptools import setup

setup(
    name="flux-3-dev-api",
    version="0.1.0",
    author="Anil Matcha",
    description="Python wrapper for Black Forest Labs' FLUX 3 Dev API — the faster, lower-cost FLUX 3 variant, plus the full FLUX 3 family (Text-to-Image, Image-to-Image, Text-to-Video, Image-to-Video).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["flux3_dev_api", "mcp_server"],
    install_requires=[
        "requests",
        "python-dotenv",
        "mcp[cli]"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
