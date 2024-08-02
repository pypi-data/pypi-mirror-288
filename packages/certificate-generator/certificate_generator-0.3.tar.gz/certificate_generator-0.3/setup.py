from setuptools import setup, find_packages

setup(
    name="certificate_generator",
    version="0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "generate-certificates=certificate_generator.generator:main",
        ],
    },
    author="Asib Hossen",
    author_email="dev.asib@proton.me",
    description="A package to generate certificates with a given name and a logo in the top middle.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/codewithasib/certificate_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
