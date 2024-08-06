from setuptools import setup, find_packages

setup(
    name="TT_auth_system",
    version="1.1.0",
    author="Jarod Johnson",
    author_email="jarodjohnson1001@gmail.com",
    description="An authentication system with one-time login links and templated email sending",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jarod-johnson-23/TT24_otc_generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'python-dotenv',
        'jinja2',
        'cryptography',
        'pymysql',
    ],
)