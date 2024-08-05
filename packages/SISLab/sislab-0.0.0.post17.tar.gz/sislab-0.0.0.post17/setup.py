from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SISLab",
    version="0.0.0-17",
    description="Inje University Department of Biomedical Engineering SISLab open source library for signal processing, image processing and AI",
    long_description="Long description of your package",
    long_description_content_type="text/markdown",
    author="Shyubi",
    author_email="sjslife97@gmail.com",
    url="https://github.com/Shyuvi/SISLab",
    packages=find_packages(include=['SISLab', 'SISLab.*']),
    # package_data={'SISLab': ['key_checker.py.enc']},
    include_package_data=True,
    install_requires=[
        "numpy", "pillow", "opencv-python", "tensorflow", "torch", 
        "scikit-learn", "scipy", "matplotlib", "cryptography"
    ],
    python_requires=">=3.8",
    keywords=["shyubi", "sislab", "signal", "image"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
