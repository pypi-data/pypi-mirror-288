# setup.py

from setuptools import setup, find_packages

setup(
    name="face_similarity",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "scikit-image",
        "scikit-learn",
        "face_recognition",
    ],
    author="Muhammad Furqan Javed",
    author_email="mfurqanjaved@gmail.com",
    description="A package to compare face similarity from documents and original image.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/face_similarity",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)