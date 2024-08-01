from setuptools import setup, find_packages

setup(
    name='llm-xs',
    version='1.0.0',
    description='A module for creation of endpoint for the OPEN-SOURCED LLMs, currently supports only text inference route.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/xprabhudayal/xs.git',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author='Prabhudayal Vaishnav',
    author_email='pradachan@tuta.io',
    license='MIT',
    py_modules=['xs'],
    install_requires=[
        'flask',
        'pyngrok',
        'waitress'
    ],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


