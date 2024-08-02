from setuptools import setup

setup(
    name="pixi-cli",
    version="0.2.1",
    py_modules=["pixi"],
    install_requires=[
        "Pillow",
        "cairosvg"
    ],
    entry_points={
        'console_scripts': [
            'pixi=pixi:main',
        ],
    },
    author="Zain Karim",
    author_email="zain@zainkarim.com",
    description="A command-line tool for basic image processing tasks.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/zainkarim/pixi-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
