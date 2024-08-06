import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weedeia-greenbox-core",
    version="0.0.19",
    author="Paulo Porto",
    author_email="cesarpaulomp@gmail.com",
    description="API for GPIO admnistration",
    packages=[
      "src",
      "src.util",
      "src.service",
      "src.constants",
    ],
    entry_points={
      "console_scripts": [
          "weedeia-greenbox-core=src.main:main",
      ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'wheel',
        'rpi.gpio'
    ]
)