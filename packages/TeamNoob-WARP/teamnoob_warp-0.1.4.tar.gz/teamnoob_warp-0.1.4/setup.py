from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TeamNoob_WARP",
    version="0.1.4",
    author="GW ROHIT",
    author_email="teamnoob909@gmail.com",
    description="A library for sending WARP MB using a referrer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://t.me/TeamNoob_Official",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "python-cfonts"
    ],
    entry_points={
        'console_scripts': [
            'tnwarp=TeamNoob_WARP.main:tnwarp',
        ],
    },
    keywords="warp teamnoob cloudflare referrer unlimited mb rohit python library",
)