from setuptools import setup, find_packages;

with open("README.md", "r") as fh:
    readMe = fh.read();

with open("requirements.txt") as f:
    required = f.read().splitlines();

with open("version.txt", "r") as fh:
    versionFile = fh.read().strip();

optional_dependencies = {
    "All": [],
    "Graphics": [
        "tkcalendar==1.6.1",
        "Babel==2.15.0"
    ],
    "PdfManager": [
        "reportlab==4.2.0",
        "pypdf==4.2.0"
    ],
    "XmlManager": [
        "lxml==5.2.2"
    ],
    "AdvancedUtils": [
        "codicefiscale==0.9"
    ]
}

setup(
    name='almax_common',
    version=versionFile,
    description='Library with my most used Classes and Methods',
    long_description=readMe,
    long_description_content_type='text/markdown',
    author='AlMax98',
    author_email='alihaider.maqsood@gmail.com',
    packages=find_packages(),
    package_dir={'': '.'},
    install_requires=[required],
    extra_require=optional_dependencies
);