from setuptools import find_packages, setup

setup(
    name="torda",
    version="0.1.6.3",
    author="limyj0708",
    author_email="limyj0708@gmail.com",
    description="Tools for Repetitive Data Analysis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/limyj0708/TORDA",
    packages=find_packages(include=['torda', 'torda.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    license='MIT',
    install_requires=[
        'plotly',
        'scipy',
        'scikit-learn',
        'pandas',
        'numpy',
    ],
)