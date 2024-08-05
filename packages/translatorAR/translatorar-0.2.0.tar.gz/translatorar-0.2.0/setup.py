from setuptools import setup, find_packages

setup(
    name='translatorAR',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'pymupdf',
        'tqdm',
        'pdf2image',
        'pytesseract',
        'pillow'
        # Add other dependencies here
    ],
    include_package_data=True,
    license='CC BY-NC 4.0',
    description='A translation tool for multiple languages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Amin Boulouma',
    author_email='amin@boulouma.com',
    url='https://pypi.org/project/translatorAR/0.1.0/',
)
