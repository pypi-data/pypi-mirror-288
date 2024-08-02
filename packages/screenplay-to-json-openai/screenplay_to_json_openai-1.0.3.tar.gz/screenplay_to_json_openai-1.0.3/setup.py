from setuptools import setup, find_packages

setup(
    name='screenplay-to-json-openai',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'openai', 'pdf2image', 'Pillow'
    ],
    author='Alexis Kirke',
    author_email='alexiskirke2@gmail.com',
    description='A tool to a screenplay PDF to JSON format using OpenAI Vision Transformer Analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
