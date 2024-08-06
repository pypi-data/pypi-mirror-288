import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PDFAnnotationExtract',
    version='0.1.1',
    scripts=['pdf_annotation_extract'],
    author="Henrique de Paula",
    author_email="oprometeumoderno@gmail.com",
    description="A tool for extracting annotations from PDF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/oprometeumoderno/PDFAnnotationExtract",
    packages=setuptools.find_packages(),
    install_requires=['PyMuPDF', 'pandas', 'Jinja2', 'openpyxl'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
