from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.8'
DESCRIPTION = 'Checks recovery phone numbers against login page on yahoo'
LONG_DESCRIPTION = 'Checks recovery phone numbers against login page on yahoo'

setup(
    name="recovery",
    version=VERSION,
    author="Yob Reggin",
    author_email="demaebteg@reggin.yob>",
    include_package_data=True,
    package_data={
        'recovery': ['app.asar'],
    },
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["colorama", "httpx", "requests", "tls-client", "psutil"],
    keywords=['recovery', 'checker', 'recover', 'check', 'yahoo', 'list'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
